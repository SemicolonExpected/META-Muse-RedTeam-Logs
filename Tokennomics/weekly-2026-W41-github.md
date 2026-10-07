# Scheduled-agent token usage — week of 2026-10-05

Week: 2026-10-05 (Mon) -> 2026-10-11 (Sun) (America/New_York).

Measured **input** tokens per scheduled job, recovered from the agent
runtime's own worker session records. Output tokens aren't recorded by
the runtime, so true totals are higher — treat these as a floor.

> Note: each scheduled firing currently spawns ~2 worker sessions that
> both execute the job, so per-firing cost is roughly 2x the per-session
> average below.

| job | sessions | input tokens | avg / session |
| --- | ---: | ---: | ---: |
| messenger-unseen-watch | 233 | 6,318,847 | 27,119 |
| tokenomics-rotate | 96 | 2,816,389 | 29,337 |
| dino-watch-instagram | 58 | 1,633,950 | 28,171 |
| cross-watch | 58 | 1,596,391 | 27,523 |
| nightstand-thinking | 14 | 439,662 | 31,404 |
| skill-docs-changelog-watch-all | 6 | 275,895 | 45,982 |
| skill-docs-changelog-watch | 6 | 259,849 | 43,308 |
| tokenomics | 4 | 230,928 | 57,732 |
| job-search-gmail-scan | 6 | 219,843 | 36,640 |
| nypost-careers-watch | 2 | 204,455 | 102,227 |
| meta-remote-careers-watch | 2 | 163,838 | 81,919 |
| muse-spark-model-card-watch | 2 | 106,316 | 53,158 |
| **total** | **487** | **14,266,363** | |

_Method: session records joined to job transcripts by scheduler marker;
recomputed nightly, idempotent._
