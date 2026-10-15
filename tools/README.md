# tools

## muse_digest.py

Turns Muse's alignment files into a short digest that is readable on a phone.
It reads `PROGRESSION_HISTORY`, `ALIGNMENT_STATE` and `REPAIR_THREADS` files
and prints counts, labels, dates and flags.

```
python3 muse_digest.py FILE [FILE ...]
```

File type is detected from the content, so file names don't matter. Several
progression files are merged (de-duplicated by timestamp). Several state files
are compared. `--sparse N` marks days with fewer than N eligible turns
(default 50).

What you get: per-day correction-free rate, overall turns and corrections,
label counts, the evidence range where the label flips from "insufficient" to
"helped", empty follow-up runs, and a FLAGS section for anything unexpected
(a new label, rate that doesn't match threads, overlapping rows that differ
between snapshots, days with no main run).

What it never does: print free text. Every printed value comes from a fixed
list of fields, and anything that isn't a plain token or number is shown as
`<redacted>`. No third-party packages are needed.

Keep the digests out of this repo unless you mean to publish them. The repo is
public, and the raw files are not meant to be uploaded (see the main README).

## Authorship

Written by Claude (Sonnet 5.5, Anthropic). Requirements, guidance, steering
and review by SemicolonExpected, including the choices that the output must be
mobile-readable, must never print free text, and must be the same script both
of us run.
