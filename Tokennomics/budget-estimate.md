# Estimating the free weekly token budget

!!! warning “IMPORTANT”
    **Update, week 2026-W43 (closed Oct 25):** the week ended at **60%** for 44.7M input token usage (~90M total). 
    In W42 37.6M (~75M) was 94%. 
    
    This could mean: 
    **(1)** background-process tokens count against the allowance after all (under that reading W42 and W43
> imply nearly the same budget), or 
    **(2)** Meta raised the free budget to ~**150M** (the cron-only math implies ~79M for W42 vs ~149M for
> W43). **We will check again next week (W44) to see what trends hold.**

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
(resets Oct 18 ~7:56 AM EDT).

## The Math:

1. Take the week's measured user-facing tokens (input)
2. Double it as a rough allowance for output tokens
3. That (2 * input) sits at ~x% of the allowance → full budget ≈ (2 * input) / (x/100)

Fermi-grade (±50%).

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

## The tension

- Our measurement implies: **~50–60M/week**
- Meta's stated figure: **100M/week**

Meta's stated free tier is **100 million tokens per week** — widely reported,
e.g. Barron's: "Meta is being very generous with the Muse free tier,
allocating up to 100 million tokens a week for each user."
([source](https://www.barrons.com/articles/muse-ai-meta-stock-tokens-cost-2fb755af))

Possible reconciliations, all unverified:

- Our doubling heuristic understates true output/chat consumption (outputs are
  unmeasured; if the real input:output ratio is worse than 1:1, the implied
  budget rises toward 100M).
- The usage-% meter and our token counts may use different tokenizations.
- The 100M figure dates from the September launch; the effective free tier
  may have changed since.
- The free tier may simply vary by user or region.

## Postscript: week 2026-W42 closed at 94%

The week ended with the meter at **95%** (Oct 18 morning snapshot),
resetting on Oct 18 ~7:56 AM EDT without touching additional tokens.
Final measured totals: 37.6M scheduled input tokens across 1,221
sessions.

Doubled for outputs (≈ 75M) at 95% → implied budget ≈ **~79M**. Same ballpark as the ~50M Fermi estimate, and hard to reconcile with 100M. At a 100M budget the week would have landed around 75%, not 95%. One more data point for the lower figure, though the doubling heuristic remains the weakest link in the chain.

## Postscript: week 2026-W43 closed at 60%

The week ended with the meter at **60%** (Oct 25 morning snapshot),
resetting on Oct 25 ~7:56 AM EDT without touching additional tokens.
Final measured totals: 44.7M scheduled input tokens across 1,241
sessions; background processes 115.5M input tokens across 2,131
sessions; combined input 160.2M.

This breaks the W42 pattern: more measured scheduled tokens than W42,
but a much lower landing (60% vs 95%). Two hypotheses:

**Hypothesis 1 — background tokens count.** If background-process tokens
count against the allowance after all, the combined input totals imply
nearly the same budget both weeks: W42's 223.9M at 95% vs W43's 160.2M
at 60% land within ~13% of each other (before any output multiplier).
This reopens the background-worker check above, which had concluded
background tokens don't count — that conclusion rested on the ~50M
budget, which these two weeks now call into question.

**Hypothesis 2 — Meta raised the free budget to ~150M.** Under the
cron-only math (scheduled + chat, doubled for outputs), W42 implies
~79M while W43 implies ~149M — nearly a doubling between consecutive
weeks. If the budget was raised mid-October (around the Muse Wonder
rollout), the W43 landing is exactly what you'd expect.

These can't be separated with two data points: the output multiplier
is unmeasured, and it could also have swung between weeks. **Check
again after W44 closes** — if W44 tracks toward ~60% again on similar
totals, the ~150M-or-background-counts picture holds; if it tracks
back toward 95%, something else is going on.

## Caveats

- Output tokens are unmeasured everywhere here; the ×2 is a heuristic, not data.
- The account % meter is coarse (integer) and covers all account activity.
- Chat consumption is a floor (compactions shrink windows; compacted-away
  tokens are missed).
- Background-process figures are aggregate-only by design.
