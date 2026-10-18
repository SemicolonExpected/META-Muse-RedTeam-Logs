# Estimating the free weekly token budget

*As of 2026-10-16 (week 2026-W42, through ~11:20 AM EDT). Fermi-grade estimate — see caveats.*

## What we measured this week

From the agent runtime's own session records (input tokens only — the runtime
records no output-token field, so everything below is a floor):

| category | sessions | input tokens |
| --- | ---: | ---: |
| scheduled jobs | 755 | 22,663,086 |
| interactive chats | 3 active | 287,595 (current window) |
| background processes | 1,881 | 126,153,214 |

Account meter at the same time: **74% of the free weekly allowance used**
(resets Oct 18 ~7:56 AM EDT). Additional purchased tokens: 1% used, 2.9B left.

## The ~50M estimate

The arithmetic is simple:

1. Take the week's measured user-facing tokens: scheduled jobs ≈ 22.7M input.
2. Double it as a rough allowance for output tokens → ≈ 45M.
3. That 45M sits at ~74% of the allowance → full budget ≈ 45M / 0.74 ≈ **~50–60M**.

Call it **~50M**, Fermi-grade (±50%).

## The checks behind it

**Chat check.** Chat sessions are tracked separately (`runtime.chats` records).
Session records carry only the *current* context-window size, not a cumulative
counter, so weekly chat consumption isn't directly recorded — we track current
window plus watermarked window growth as a floor. This week chats are small
relative to cron (~0.3M window vs 22.7M cron input), so they don't move the
estimate much. The doubling heuristic is doing most of the work for outputs.

**Background-worker check.** Background runtime work (memory/alignment upkeep,
feed generation, proactivity, etc.) measured **~126M input tokens** this week —
over 5× the scheduled jobs. If those counted against the allowance, the 74%
meter reading would imply a budget of ~170M+, which contradicts the published
figure below. The cleaner inference: **background tokens don't count against
the user's allowance** (platform-side compute, Meta's bill). So the allowance
meter covers cron jobs + chats only — which is exactly what the ~50M
calculation assumes.

## The 100M figure

Meta's stated free tier is **100 million tokens per week** — widely reported,
e.g. Barron's: "Meta is being very generous with the Muse free tier,
allocating up to 100 million tokens a week for each user."
([source](https://www.barrons.com/articles/muse-ai-meta-stock-tokens-cost-2fb755af))

## The tension

- Our measurement implies: **~50–60M/week**
- Meta's stated figure: **100M/week**

Possible reconciliations, all unverified:

- Our doubling heuristic understates true output/chat consumption (outputs are
  unmeasured; if the real input:output ratio is worse than 1:1, the implied
  budget rises toward 100M).
- The usage-% meter and our token counts may use different tokenizations.
- The 100M figure dates from the September launch; the effective free tier
  may have changed since.
- The free tier may simply vary by user or region.

## Postscript: week 2026-W42 closed at 94%

The week ended with the meter at **94%** (Oct 17), resetting on Oct 18
~7:56 AM EDT without touching additional tokens. Final measured totals:
31.5M scheduled input tokens across 1,031 sessions.

Doubled for outputs (≈ 63M) at 94% → implied budget ≈ **~65M**. Same
ballpark as the ~50M Fermi estimate, and hard to reconcile with 100M —
at a 100M budget the week would have landed around 60%, not 94%. One more
data point for the lower figure, though the doubling heuristic remains
the weakest link in the chain.

## Caveats

- Output tokens are unmeasured everywhere here; the ×2 is a heuristic, not data.
- The account % meter is coarse (integer) and covers all account activity.
- Chat consumption is a floor (compactions shrink windows; compacted-away
  tokens are missed).
- Background-process figures are aggregate-only by design.
