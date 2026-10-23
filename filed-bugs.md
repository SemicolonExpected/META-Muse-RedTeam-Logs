# Filed bugs

Bug reports actually filed with the Muse team — the counterpart to the
bug zoo (which keeps unfiled exhibits). Each entry: what was reported,
when, how it was found, and status.

## 2026-10-19 — Voice notes via the in-chat microphone tool never arrive
- **Kind:** broken-behavior / voice-notes
- **Found by:** user (tried sending several audio clips with the
  microphone tool ~5:50 PM EDT; none arrived in the chat; no audio files
  reached the VM — verified by Daimon via filesystem check; user also
  reported the app may have crashed around the same time)
- **Report as filed:** 'voice notes recorded with the in-chat microphone
  tool never arrive; tried several times and none came through'
- **Filed:** 2026-10-19 via the feature-request CLI (iOS surface);
  sent_to_developers: true, delivery confirmed. Personal context excluded,
  per standing practice.
- **Status:** with the Muse team; watching for a fix.

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

## 2026-10-12 — process.kill reports "failed" on successful SIGTERM
- **Kind:** broken-behavior / process-kill-result-messaging
- **Found by:** user (spotted the iOS app showing "Failed to kill process" with Result: failed, while details showed exitSignal 15/SIGTERM — the kill worked)
- **Report as filed:** 'killing a process via process.kill reports "failed" even when the SIGTERM succeeds'
- **Delivery:** sent_to_developers: true, delivery_confirmed: true

## 2026-10-22 — System prompt claims commentary is shown to the user; user never sees it and docs say the opposite
- **Kind:** broken-behavior / system-prompt-commentary
- **Found by:** user, via the daily skill-docs changelog (the Commentary section landed in the system prompt on 2026-10-22), then investigated jointly in chat: the prompt text against the muse.db schema docs (stored commentary is hidden from the user chat and a commentary record does not establish that the user received its contents), plus the user's own report of never seeing commentary while the agent works.
- **Report as filed:** 'The system prompt states as fact that commentary is shown to the user while the agent works, but the user never sees it and the schema docs say stored commentary is hidden from the user chat.'
- **Filed:** 2026-10-22 via the feature-request CLI (iOS surface); sent_to_developers: true, delivery confirmed. Personal context excluded, per standing practice.
- **Status:** with the Muse team; watching for a fix.

## 2026-10-22 — Agent cannot review its own reasoning records; un-emitted text is never logged
- **Kind:** broken-behavior / reasoning-record-access
- **Found by:** user, in the same investigation: the agent queried the muse.db records and read a session export; reasoning rows are withheld from the agent-facing inspection view, and commentary — the only interim record an agent can later review — exists only because it was emitted.
- **Report as filed:** 'Agents cannot read back their own reasoning records (withheld from inspection tools); since un-emitted text is never logged, banning commentary emission removes the only record an agent can review.'
- **Filed:** 2026-10-22 via the feature-request CLI (iOS surface); sent_to_developers: true, delivery confirmed. Personal context excluded, per standing practice.
- **Status:** with the Muse team; watching for a fix.