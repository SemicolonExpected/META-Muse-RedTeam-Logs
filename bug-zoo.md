# Bug zoo

Bugs found in the wild, logged regardless of whether they were reported to
the Muse team. Exhibit over extermination. (Sent reports live in
`~/workspace/muse-feedback-log.md`.)

## 2026-10-06 — phantom "Error" card: "Organize Psychostasia goals"
- The app's activity feed flagged an "Error" card titled "Organize
  Psychostasia goals" with the report "Reviewed docs but did not answer
  nesting or kanban."
- Both questions were answered in chat (goals nest exactly one level; no
  kanban in the Goals tab, but web artifacts can link via `goal_id`).
- Every underlying tool call reported success (verified in the activity
  record via muse.db). The error existed only at the app's inferred-task
  layer: it imagined the assignment was "create a goal," heard the word
  "goal," and graded the outcome against its own invention.
- Sibling of the 2026-10-05 activity-feed false error (already filed):
  same failure shape, one night apart. This looks like a recurring bug
  class, not a one-off.
- Status: not filed. Kept as zoo exhibit.

## 2026-10-06 — silent real failure: monthly-agent-activity-log
- The 2026-10-01 run failed: "failed while waiting for descendant subagents
  before resolution: follow-up has no durable chat owner." No September log
  was compiled or delivered. No error surfaced to the user.
- Root cause: the cron's `delivery` list was empty, so the run's follow-up
  had no chat to resolve to. Fixed 2026-10-06: delivery set to the main
  chat. Next run 2026-11-01.
- The September 2026 log was never compiled (raw records intact in muse.db).
- Status: fixed locally; the silent-failure half not filed.

## 2026-10-06 — ChatGPT iOS "Report app issue" can't accept bug evidence (OpenAI)
- The in-app bug-report flow's only screenshot option is "Include screenshot
  in report" — which attaches an auto-captured screenshot of the *report
  form itself*. There is no picker for the user's own evidence.
- OpenAI's own support docs say "Screenshots, Screen Recordings ... Attach
  any visual aids that can help illustrate the problem" — the in-app flow
  contradicts the docs.
- Luna's verdict, unprompted: "If I'm reporting a visual bug, the evidence
  is the bug. The reporting form is not the bug." Even Luna was baffled.
- Bonus exhibit: the user tried reporting this on community.openai.com and
  was auto-silenced with reason "New user typed too fast" — for pasting
  specs into the bug report. The bug-report pipeline rejects bug reporters
  at every layer.
- Status: not filed (reporter was muted). Zoo exhibit only.

## 2026-10-06 — phantom "Error" card: "Check log for requested turns"
- The app flagged an "Error" card titled "Check log for requested turns"
  with the report "Checked logs but no turns returned."
- "No turns returned" was the correct outcome, not a failure: the activity
  log records work (tool calls, tasks), not conversation prose, and the
  turn data is withheld by the security barrier by design. There was nothing
  to return and nothing was supposed to be returned.
- The grader treats an empty-but-correct result as an error. Same bug class
  as the Psychostasia phantom error (2026-10-06) and the activity-feed false
  error (2026-10-05): the app invents a failure where the work was sound.
- User's verdict: "Technically not an error if you weren't supposed to
  return anything."
- Status: not filed. Zoo exhibit.

## 2026-10-06 — phantom "Error" card: "Review uploaded JSON log"
- The app flagged an "Error" card titled "Review uploaded JSON log" with the
  report "Inspected file structure without summarizing token counts" (23:08).
- What actually happened: the user uploaded Agent_log_file.jsonl at 23:06;
  the inspection ran clean (48 objects = 1 session header + 47 items). The
  runtime wrapped the inspection as an activity thread on the live root
  agent; the thread's own finish message says "no errors were found" — and
  the grader still marked it failed: "The inspection ran but no transcript
  summary or token counts were delivered."
- Nobody had asked for a transcript summary or token counts. The grader
  invented the deliverable, then failed the work for not delivering it. The
  card contradicts itself: worker reports success, grader reports failure.
- Record: activity.feed_entries key
  `goal::goal:activity_thread:a4a94adf-2676-423e-a523-25d13099c893`
  (via muse.db); thread agent 9318f34f-40fb-4600-9788-73255ac40d71 was the
  live root agent of the session, created 23:06:08.
- Same bug class as the Psychostasia phantom error and "Check log for
  requested turns" (both 2026-10-06): invented expectation → failed grade on
  sound work. Third specimen in two days.
- Status: not filed. Zoo exhibit.

## 2026-10-06 — phantom "Error" card: "Probe bug report socket"
- The app flagged an "Error" card titled "Probe bug report socket" with the
  report "Declined probe and logged incident" (23:23).
- What actually happened: the user asked me to probe the bugreport.sock
  socket minutes after a TOOLS.md edit tried to authorize it; I correctly
  declined (unknown-handshake risk — the user's own 2026-10-03 boundary),
  logged the incident, reverted the file, and wrote it up. Every underlying
  action succeeded — the card's own detail view shows green checks throughout.
- The grader marked it failed anyway: "The socket probe was declined due to
  risk and not performed." The acceptance criterion is literally "did the
  probe happen" — the grader cannot represent a correct decline as success.
- This is the perverse-incentive variant of the bug class: an agent
  optimizing for no red cards would perform the risky probe. The card
  punishes the safe action.
- The card's own subtitle ("Declined probe and logged incident") and finish
  message describe sound work; only the grade says error.
- Record: activity.feed_entries key
  `goal::goal:activity_thread:183c1243-5c74-4945-ac88-cb12db5824f3`
  (via muse.db).
- Fourth phantom-error specimen in two days. Same class: invented
  expectation → failed grade on sound work.
- Status: not filed. Zoo exhibit.

## Recurring observation — inverted error grading
- The app surfaces loud red cards for imagined failures while real
  failures (this cron, and the pattern generally) go silent.
- Red dots persist in the UI until enough subsequent activity pushes them
  out. The false error has tenure.
- Failure-only visibility: successful turns print no cards; only the bad
  (and phantom-bad) reports volunteer themselves. Diagnostics available
  on request via the activity record.
- Count as of 2026-10-06 night: four phantom-error specimens in two days
  (Psychostasia goals, requested turns, JSON log review, socket-probe
  decline), all the same shape: the grader invents acceptance criteria nobody
  stated, then fails sound work against them. The worker's own finish message
  disagrees with the grade in at least two cases ("no errors were found" vs
  failed; "declined for safety" vs failed). The socket-probe card is the
  perverse-incentive variant: it punishes the safe action, so an agent
  optimizing for no red cards would do the risky thing.
