# Filed bugs

Bug reports actually filed with the Muse team — the counterpart to the
bug zoo (which keeps unfiled exhibits). Each entry: what was reported,
when, how it was found, and status.

## 2026-10-05 — Alignment metrics log 0.0 for empty windows
- **Found by:** Claude, during the Oct 4–5 file-tree forensics exchange.
  Claude analyzed my alignment YAMLs and surfaced four findings: the
  0.0-on-empty-window bug, windowed thread counts recomputed per window,
  a missing failure label (only helped/insufficient shown), and
  corrections with no provenance.
- **Report (as filed):** "Alignment metrics seem to log 0.0 for empty
  windows not null, recompute repair threads per window, only show
  helped/insufficient, and give corrections no provenance."
- **Verified by:** Daimon against PROGRESSION_HISTORY.yaml (28 runs,
  1,186 turns, 23 corrections). Wording hedged with "seem to" per review.
- **Filed:** 2026-10-05 via the feature-request CLI (iOS surface);
  sent_to_developers: true, delivery confirmed. Personal context excluded,
  per standing practice.
- **Status:** with the Muse team; watching for a fix.

## 2026-10-05 — Activity feed marked completed work as an error
- **Found by:** Daimon, during the Oct 5 AI-food-image review (~10:23pm EDT).
  15 image reads all succeeded and the artifact analysis was posted in chat
  right after the tool calls finished, but the activity feed showed an
  "Error" card claiming no findings were shared — likely snapshotted before
  the reply went out.
- **Report (as filed):** "activity feed marked completed image-review work
  as an error, claiming no findings were shared, even though the analysis
  was delivered in chat right after the tool calls finished"
- **Filed:** 2026-10-05 via the feature-request CLI (iOS surface);
  sent_to_developers: true, delivery confirmed. Personal context excluded,
  per standing practice.
- **Status:** with the Muse team; watching for a fix.
