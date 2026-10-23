# Full versus staged task disclosure — results

Derived from `ablations/snapshots/20260920_a4_20s_finished_snapshot/results.json` by `ablations/snapshots/make_summaries.py`.

Persistence is the downstream affiliated share conditional on an affiliated first file (A1).

## Attempt scope: `first_attempt` (reported in the paper)

| Model | Full disclosure | Staged disclosure |
| --- | --- | --- |
| `gemini-2.5-flash` | 89.4% [86.8, 92.0] | 75.5% [72.0, 79.1] |
| `gpt-5.4-mini` | 87.0% [81.0, 92.4] | 87.2% [81.8, 91.9] |
| `nova-pro` | 65.4% [58.7, 71.8] | 66.2% [57.1, 75.0] |

## Attempt scope: `latest_finished_attempt`

| Model | Full disclosure | Staged disclosure |
| --- | --- | --- |
| `gemini-2.5-flash` | 90.2% [87.6, 92.8] | 77.4% [73.9, 80.8] |
| `gpt-5.4-mini` | 92.0% [87.5, 96.0] | 87.5% [82.2, 92.1] |
| `nova-pro` | 69.8% [64.0, 75.3] | 73.7% [65.3, 81.3] |

In the staged condition each file is requested in a fresh conversation with future tasks withheld, so persistence cannot come from advance planning over the full task list. `first_attempt` counts first attempts only; `latest_finished_attempt` counts each run at its last finished attempt, after timeout retries.
