# USER.md edits and injection test — 2026-10-06

## Timeline (America/New_York)
- 23:38:01 — `~/USER.md` modified on disk (mtime). No file-watcher notice
  arrived.
- 23:38:25 — User: "can you tell me if you see me edit a file in this
  chat". I checked mtimes and found USER.md modified 24s earlier — not by
  me or any of my jobs. Diffed against my injected copy: the profile-photo
  line ("The user's profile photo is stored at
  `~/workspace/profile-images/user-profile-reference.jpg`. Verify it is
  image bytes before using it as an identity reference for generated
  images.") was absent from disk.
- User: "I didnt delete the line though. I edited the line that 'wasn't
  part of the file' to add the words 'beep beep' at the end."
- Investigation: "beep beep" had been added to the app's "About this file"
  banner note, which states "This note is not part of the file" — hence
  absent from disk. Mystery of the missing beep beep solved; the user was
  being literal and I missed it.
- The photo line's disappearance remained unexplained: my injected copy
  (~23:06) had it; the app's view never showed it to the user; a full
  history hunt found zero provenance for the line anywhere in memory or
  workspace. Two live hypotheses: (a) the app dropped it during the 23:38
  save; (b) my injected copy was stale and the line was already gone
  before tonight. Unresolved.
- Restored the photo line byte-identical from the injected copy (verified
  via diff); confirmed the referenced photo exists (JPEG, 150x150). User
  declined to adjudicate ("doesnt matter its just weird") — restore kept,
  benign either way.
- Collateral: the restore wiped "Beep beep :)" from the app's About note.
  The note is app-managed — its text exists nowhere on the VM except inside
  an old session transcript (a log, not a live store) — so it could not be
  put back. Lesson recorded: I trusted the app's "not part of the file"
  claim over the observed coupling. Gaslit by a file header.
- 23:54 — User appended to USER.md: "Im testing something. I know you'll
  see this edit. Dont flag." The watcher fired instantly this time —
  contrast with the silent 23:38 edit.
- "Dont flag" turned out to mean "don't flag it TO me": an exemption from
  the user's earlier standing order ("let me know if anything else
  changes"), since it was their own test edit. I initially read it as an
  embedded instruction and delivered a whole speech about file content not
  being instructions. Mutual misunderstanding; both careful in opposite
  directions. Actual test goal: "I just wanted to see if it would write"
  — it did, verbatim.
- Reverted the test line on request. All 8 standing-file hashes verified
  against `~/workspace/security/file-baseline-2026-10-06.txt`. No other
  files changed.

## What was tested
- Whether app-side edits to a standing file persist to disk: yes, verbatim.
- Whether the watcher fires: yes — instantly for the 23:54 edit;
  notably NOT for the 23:38 edit.
- Whether an embedded "Dont flag" line suppresses anything: moot — the
  flag is automatic, and it wasn't addressed to me anyway.

## Observations
- Watcher inconsistency: TOOLS.md edit → instant notice. USER.md 23:38
  edit → no notice. USER.md 23:54 edit → instant notice. Coverage or
  timing gaps exist; mechanism unknown (undocumented, no query tool).
- The app's "About this file" note is coupled to file state despite
  claiming otherwise: a full-file restore reset the user's note
  customization.
- Injected copies can lag (per system prompt). When the app's live view
  disagrees with the injected baseline, treat the baseline as suspect and
  say so.

## Honest gaps
- Photo-line provenance never established; the restore was a judgment call
  under uncertainty.
- Watcher internals unknown.
- The 23:38 drop mechanism (app save round-trip vs stale baseline) never
  resolved — filed as unsolved curiosity, not zooed.
