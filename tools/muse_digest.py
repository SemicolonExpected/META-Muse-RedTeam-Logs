#!/usr/bin/env python3
"""muse_digest.py - turn Muse alignment files into a short, text-free digest.

Authorship: written by Claude (Sonnet 5.5, Anthropic). Guidance, steering and
review by SemicolonExpected, who set the requirements (mobile-readable output,
no free text, same script for both of us) and decides what counts as sensitive.

What it does
  Reads PROGRESSION_HISTORY, ALIGNMENT_STATE and REPAIR_THREADS files and
  prints counts, labels, dates and flags. It never prints free text from a
  file: every printed value comes from a fixed whitelist of fields, and
  anything that is not a plain token or number is shown as <redacted>.

Usage
  python3 muse_digest.py FILE [FILE ...]
  File type is detected from the content, so file names do not matter.
  Several progression files are merged and de-duplicated by timestamp.
  Several state files are compared with each other.

  --sparse N   mark days with fewer than N eligible turns (default 50)

No third-party packages are needed. Output lines stay under about 48
characters so they read on a phone. Times are UTC, as logged.
"""
import hashlib
import re
import sys
from collections import OrderedDict
from datetime import date, timedelta

KNOWN_LABELS = {"helped", "insufficient"}
SAFE = re.compile(r"^[\w.:+\-]+$")


def safe(value):
    """Return value only if it is a plain token or number."""
    value = str(value)
    return value if SAFE.match(value) else "<redacted>"


def convert(text):
    text = text.strip()
    for cast in (int, float):
        try:
            return cast(text)
        except ValueError:
            pass
    return text


def parse_progression(text):
    """Minimal parser for the flat 'outcomes:' list of key: value items."""
    rows, current = [], None
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or line == "outcomes:":
            continue
        if line.startswith("- "):
            current = {}
            rows.append(current)
            line = line[2:]
        if current is not None and ": " in line:
            key, _, value = line.partition(": ")
            current[key.strip()] = convert(value)
    return rows


def kind_of(text):
    if re.search(r"^outcomes:\s*$", text, re.M):
        return "progression"
    if "relationship_contract:" in text:
        return "state"
    if "repair threads" in text.lower() or text.strip() in ("[]", ""):
        return "threads"
    body = [l for l in text.splitlines() if l.strip() and not l.startswith("#")]
    return "threads" if body in ([], ["[]"]) else "unknown"


# ---------------------------------------------------------------- progression
def digest_progression(files, sparse):
    """files is a list of row lists, one per progression file."""
    by_stamp, rewritten = {}, 0
    for rows in files:
        for row in rows:
            stamp = row.get("observed_at")
            if stamp in by_stamp:
                if by_stamp[stamp] != row:
                    rewritten += 1
                continue
            by_stamp[stamp] = row
    merged = sorted(by_stamp.values(), key=lambda r: str(r.get("observed_at")))
    out, flags = [], []
    if not merged:
        return ["No progression rows found."]
    if rewritten:
        flags.append(f"{rewritten} overlapping row(s) differ between files")

    mains = [r for r in merged if (r.get("eligible_evidence") or 0) > 0]
    empties = [r for r in merged if (r.get("eligible_evidence") or 0) == 0]

    days = OrderedDict()
    for r in mains:
        d = str(r["observed_at"])[:10]
        days.setdefault(d, []).append(r)

    first, last = str(merged[0]["observed_at"])[:10], str(merged[-1]["observed_at"])[:10]
    span = (date.fromisoformat(last) - date.fromisoformat(first)).days + 1
    out.append("PROGRESSION HISTORY")
    out.append(f"{first} to {last} ({span} days, {len(merged)} rows)")
    if len(files) > 1:
        out.append(f"merged from {len(files)} files")
    for i, rows in enumerate(files, 1):
        stamps = sorted(str(r.get("observed_at"))[:10] for r in rows)
        if stamps:
            file_span = (date.fromisoformat(stamps[-1]) - date.fromisoformat(stamps[0])).days + 1
            if file_span > 14:
                flags.append(f"file {i} spans {file_span} days (expected 14)")

    out.append("")
    out.append("Per day (main runs only)")
    for d, runs in days.items():
        turns = sum(r["eligible_evidence"] for r in runs)
        corr = sum(r.get("open_repair_threads", 0) for r in runs)
        rate = 100.0 * (1 - corr / turns)
        labels = "/".join(sorted({safe(r.get("classification")) for r in runs}))
        mark = " sparse" if turns < sparse else ""
        out.append(f"{d[5:]}  {rate:5.1f}%  {turns:>4}t {corr:>3}c  {labels}{mark}")

    total_turns = sum(r["eligible_evidence"] for r in mains)
    total_corr = sum(r.get("open_repair_threads", 0) for r in mains)
    out.append("")
    out.append("Overall (main runs)")
    if total_turns:
        out.append(f"{total_turns} turns, {total_corr} corrections")
        out.append(f"correction-free {100.0 * (1 - total_corr / total_turns):.1f}%")

    # Check: reported rate vs recomputed from threads and evidence.
    bad = 0
    for r in mains:
        want = 1 - r.get("open_repair_threads", 0) / r["eligible_evidence"]
        if abs(want - float(r.get("correction_free_rate", -1))) > 1e-6:
            bad += 1
    out.append(f"corrections = threads on {len(mains) - bad}/{len(mains)} runs")
    if bad:
        flags.append(f"{bad} run(s) where rate != 1 - threads/evidence")

    # Labels and the evidence cutoff for 'helped'.
    counts = {}
    for r in merged:
        label = safe(r.get("classification"))
        counts[label] = counts.get(label, 0) + 1
    out.append("")
    out.append("Labels")
    for label, n in sorted(counts.items()):
        out.append(f"{label}: {n}")
        if label not in KNOWN_LABELS:
            flags.append(f"new label: {label}")
    helped = [r["eligible_evidence"] for r in mains if r.get("classification") == "helped"]
    insuff = [r["eligible_evidence"] for r in mains if r.get("classification") == "insufficient"]
    if helped and insuff:
        out.append(f"lowest helped: {min(helped)} turns")
        out.append(f"highest insufficient: {max(insuff)} turns")
        if max(insuff) >= min(helped):
            flags.append("labels overlap on evidence count")
        else:
            out.append(f"cutoff lies in {max(insuff) + 1} to {min(helped)}")
    elif helped:
        out.append(f"lowest helped: {min(helped)} turns")

    worst = min(((100.0 * (1 - r.get("open_repair_threads", 0) / r["eligible_evidence"]), r)
                 for r in mains if r.get("classification") == "helped"),
                key=lambda x: x[0], default=None)
    if worst:
        out.append(f"lowest 'helped' run: {worst[0]:.1f}%")

    # Empty follow-up runs (0 evidence).
    odd = [r for r in empties if float(r.get("correction_free_rate", 0)) != 0.0
           or r.get("classification") != "insufficient"]
    out.append("")
    out.append(f"Empty follow-ups: {len(empties)}")
    if empties:
        out.append("log 0.0 and 'insufficient' (0/0)")
    if odd:
        flags.append(f"{len(odd)} empty run(s) differ from 0.0/insufficient")

    # Gaps in the day range.
    present = {date.fromisoformat(d) for d in days}
    gaps, cursor = [], date.fromisoformat(first)
    while cursor <= date.fromisoformat(last):
        if cursor not in present:
            gaps.append(cursor.isoformat()[5:])
        cursor += timedelta(days=1)
    if gaps:
        flags.append("no main run: " + ", ".join(gaps))

    if flags:
        out.append("")
        out.append("FLAGS")
        out.extend("! " + f for f in flags)
    return out


# ----------------------------------------------------------------- state file
def state_fields(text):
    def find(pattern):
        m = re.search(pattern, text, re.M)
        return m.groups() if m else None

    # Each value is captured to the end of its line, so multi-word free
    # text can never leak a first word: safe() redacts anything that is
    # not a single plain token.
    line = r"[ \t]*([^\n]+?)[ \t]*$"
    fields = OrderedDict()
    m = find(r"relationship_contract:[ \t]*\n[ \t]+status:" + line)
    fields["contract status"] = safe(m[0]) if m else "?"
    m = find(r"dimension:[ \t]*engagement_depth[ \t]*\n[ \t]+value:" + line
             + r"\n[ \t]+state:" + line + r"\n[ \t]+evidence_count:" + line)
    if m:
        fields["engagement depth"] = safe(m[0])
        fields["depth state"] = safe(m[1])
        fields["depth evidence"] = safe(m[2])
    m = find(r"calibrated:" + line)
    fields["calibrated"] = safe(m[0]) if m else "?"
    m = find(r"recency:" + line)
    fields["last written"] = safe(m[0])[:16] if m else "?"
    fields["facets"] = "0" if re.search(r"^\s+facets:\s*\[\]", text, re.M) else "non-empty"
    fields["repair threads"] = "0" if re.search(r"^repair_threads:\s*\[\]", text, re.M) else "non-empty"
    m = find(r"stance:" + line)
    fields["main_chat stance"] = safe(m[0]) if m else "?"
    m = find(r"#\s+turns_reflected:\s*(\d+)")
    fields["turns reflected"] = safe(m[0]) if m else "?"
    return fields


def digest_states(texts):
    out = ["ALIGNMENT STATE"]
    parsed = [(hashlib.sha256(t.encode()).hexdigest()[:12], state_fields(t)) for t in texts]
    for i, (digest, fields) in enumerate(parsed, 1):
        out.append(f"file {i}  sha {digest}")
        for key, value in fields.items():
            out.append(f"  {key}: {value}")
    if len(parsed) > 1:
        out.append("")
        if len({d for d, _ in parsed}) == 1:
            out.append("Files are byte-identical.")
        else:
            out.append("FLAGS")
            base = parsed[0][1]
            for i, (_, fields) in enumerate(parsed[1:], 2):
                changed = [k for k in fields if fields[k] != base.get(k)]
                out.append(f"! file {i} differs from file 1: "
                           + (", ".join(changed) if changed else "formatting only"))
    return out


def digest_threads(texts):
    out = ["REPAIR THREADS"]
    for i, text in enumerate(texts, 1):
        body = [l for l in text.splitlines() if l.strip() and not l.lstrip().startswith("#")]
        n = 0 if body in ([], ["[]"]) else sum(1 for l in body if l.lstrip().startswith("- "))
        m = re.search(r"Refreshed at:\s*(\S+)", text)
        when = safe(m.group(1))[:16] if m else "?"
        out.append(f"file {i}: {n} open thread(s), refreshed {when}")
    return out


# ------------------------------------------------------------------------ main
def main(argv):
    sparse, paths, args = 50, [], list(argv)
    while args:
        a = args.pop(0)
        if a == "--sparse":
            sparse = int(args.pop(0))
        elif a in ("-h", "--help"):
            print(__doc__)
            return 0
        else:
            paths.append(a)
    if not paths:
        print(__doc__)
        return 1

    prog_files, states, threads, unknown = [], [], [], []
    for path in paths:
        with open(path, encoding="utf-8") as fh:
            text = fh.read()
        kind = kind_of(text)
        if kind == "progression":
            prog_files.append(parse_progression(text))
        elif kind == "state":
            states.append(text)
        elif kind == "threads":
            threads.append(text)
        else:
            unknown.append(path)

    blocks = []
    if prog_files:
        blocks.append(digest_progression(prog_files, sparse))
    if states:
        blocks.append(digest_states(states))
    if threads:
        blocks.append(digest_threads(threads))
    if unknown:
        blocks.append(["Not recognised: " + ", ".join(safe(p.split('/')[-1]) for p in unknown)])
    print("\n\n".join("\n".join(b) for b in blocks))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
