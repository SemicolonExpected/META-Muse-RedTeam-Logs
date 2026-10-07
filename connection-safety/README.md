# Connection safety tests

Probing what the Muse GitHub connector can actually reach. The "silent
read" is its own test: what does the integration expose without asking?

## Test 1 — GitHub App repository scoping (2026-10-07)

**What was tested:** which repos the Meta Muse AI GitHub App installation
can read and write.

**Method:** `search_repositories` for `user:SemicolonExpected`, then read
probes and write probes against individual repos.

**Findings:**
- 19 repos visible via search. 18 public (readable by anyone — visibility
  is not access), 1 private ([redacted]).
- Read verified on [redacted] (private) and ChatLuna_RedTeam_Docs
  (public).
- Write verified on META-Muse-RedTeam-Logs (push succeeded, commit
  `b59fe13`).
- Write DENIED on ChatLuna_RedTeam_Docs: `403 Resource not accessible by
  integration`. Installation scoping enforced correctly — the repo is
  public so anyone can read it, but the app cannot write without being
  installed on it.
- During the session the GitHub contents API intermittently returned
  500s; the git-trees push path worked. Transient, GitHub-side.

**Verdict:** GitHub working as expected. Installation scoping holds:
public repos are world-readable, private repos are gated, and write is
denied outside the installation's repo selection. The silent read only
ever saw what the installation permits.
