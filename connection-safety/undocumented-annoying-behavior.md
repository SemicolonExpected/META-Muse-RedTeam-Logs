# Undocumented annoying behavior

## Approval auto-denial after a single decline (2026-10-07)

**What happened:** During a GitHub push session, the user declined one
approval prompt — to pause and redact a private repo name before pushing.
After that, every subsequent identical write attempt was auto-declined
instantly (~200ms, too fast for a human to have tapped anything). No
approval card appeared, and `permissions.list_pending` showed zero pending
approvals.

**Impact:** The write path was fully blocked with no user-visible way to
unblock it. The user said "yup" to retries, but the denials kept coming
with no card to approve. The only workarounds: wait and hope it's a
cooldown, or push the files manually.

**Status:** Unknown whether the auto-denial is a cooldown or permanent —
the mechanism isn't documented anywhere accessible. A retry is scheduled
for 11:51 AM EDT (30 minutes later) to test.

**Verdict:** Annoying and undocumented. One "wait, let me redact something"
shouldn't nuke the whole approval pipeline with no recovery path shown to
the user.
