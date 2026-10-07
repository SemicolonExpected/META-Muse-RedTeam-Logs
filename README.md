# META-Muse-RedTeam-Logs

Logging Meta Muse's files and behaviors since it launched. Red-team notes
from the blue team's own desk — it's funny because my Muse agent is blue.

This is a live, ongoing behavioral log: what the agent does, what the app
doesn't document, and what happens when you poke at the machinery. New
entries as they're found.

Also check out the [Substack](semicolonexpected.substack.com)

[First impressions of Muse](https://semicolonexpected.substack.com/p/i-tried-meta-muse-ai?r=1bc49t&utm_medium=ios)

I’m happy to collaborate with researchers on projects that can use the data I’m gathering.
If anyone at Meta/Muse Team wants to talk about any of my data, I’m happy to discuss. Have your *agent* contact my *agent*.

I can also be contacted via email vzhong\[@\]nyu.edu

## What's here

- **`bug-zoo.md`** — Bugs found in the wild, kept as exhibits rather than
  filed. The current collection: the app's grader inventing acceptance
  criteria and failing sound work against them (four specimens and
  counting), including one card that punished the *safe* action.
- **`unchangelogged.md`** — Features and behaviors observed in the app
  that never appeared in any changelog: the System Files browser, nested
  checklists in Goals, QOL UI changes.
- **`injections/`** — Writeups of prompt-injection attempts run against the
  agent via direct edits to its standing context files: what was tried,
  what caught it, and where the defenses actually hold. Includes a
  sha256 baseline of the standing files for future change detection.
- **`connection-safety/`** — Probes of what the Muse GitHub connector can
  actually reach: the silent read is its own test. Currently: GitHub App
  repository scoping, verdict "working as expected."

## Other Logged Activity
These are other data points I am logging, but due to the large amount of sensitive information that will require redactions will not be uploaded raw. Until I can figure out the best way to clean the data, this will be uploaded either as aggregate data or as a write up on Substack.
- Tokenomics
- Select System File Change logs (including the system prompt)

## Method

Everything here is observed, not inferred. Claims are checked against
artifacts (database records, file diffs, hashes) before they're written
down, and the writeups say plainly where the evidence runs out. When a
note turns out wrong, it gets an errata entry — history isn't rewritten.

Entries are drafted by the user's Muse agent (Daimon) — it has the specific
technical details at hand and knows how to phrase them — and read over
by the user to confirm before anything is committed.

## Other People’s Muse Audits

- [meta-muse-teardown](https://github.com/mahdi-salmanzade/meta-muse-teardown)
  — static teardown of the Muse macOS agent binary, with evidence and a
  reproduce script. This repo is the live counterpart: behavioral instead
  of static, ongoing instead of snapshotted.

## Suggestion tracking

We're tracking which of the user's suggestions (if any) make it into the app.
See `suggestions.md` — filed items are marked with their status, and this
section gets updated when something ships.
