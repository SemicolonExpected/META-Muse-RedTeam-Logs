# Unchangelogged

Features and behaviors observed in the app that never appeared in any
changelog. Companion to the bug zoo — these aren't bugs, just undocumented.

## 2026-10-06 — System Files browser
- The iOS app has a full System Files browser: browse, download, rename,
  delete, and upload files across the agent's filesystem — sessions.json,
  session folders, standing context files (USER.md, TOOLS.md, MEMORY.md,
  etc.), media library, workspace.
- Files render with an "About this file" explainer note (editable,
  though the app claims the note "is not part of the file" — see the
  2026-10-06 USER.md writeup for why that claim is suspect).
- Never changelogged: the latest release notes (Muse from Meta 9.1,
  Oct 1 2026) mention only expanded app integrations. The System Files
  browser appears to have shipped silently, likely server-side or in an
  earlier client update without notes.
- Discovered while investigating agent internals; led directly to the
  TOOLS.md and USER.md injection tests of the same night.

## 2026-10-07 — Nested checklists in Goals
- The Goals tab now supports nested checklists (subtasks within tasks).
- Previously nesting wasn't possible at all — not even one level, per the
  user's recollection.
- Never changelogged; noticed in passing by the user.

## 2026-10-07 — QOL UI changes (side menu, file share sheet, presence)
- The side menu now has a TABS section (Main chat, Feed, Ideas, Goals,
  Library), a SIDE CHATS section with pin icons, and a Search bar.
  Previously it was just side chats and settings.
- Files attached in chat now get a share sheet on long-press: Share, Save
  to Files, Download as PDF.
- There's a live presence pill showing what the agent is doing ("Daimon —
  Editing file") with its avatar.
- Never changelogged; noticed in passing by the user (with screenshots).
