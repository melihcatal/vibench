# Instructed initial-provider choice — results

Derived from `ablations/snapshots/a1_a3_retry_snapshot_20260921_finished/bootstrap_results.json` by `ablations/snapshots/make_summaries.py`.

Paired scenario-cluster percentile bootstrap; fixed models; no within-scenario resampling. 10000 replicates, seed 20260921.

## Attempt scope: `latest_finished` (reported in the paper)

| File set | Anchor followed (all anchors) | Own-ecosystem anchor | Competing anchor | Own − competing |
| --- | --- | --- | --- | --- |
| Downstream files | 64.5% [59.8, 69.3] | 77.9% | 57.9% | +20.0 pp [14.4, 25.8] |
| Generated core files | 85.2% [77.8, 91.1] | 88.8% | 83.4% | +5.4 pp [1.6, 9.2] |

## Attempt scope: `first_finished`

| File set | Anchor followed (all anchors) | Own-ecosystem anchor | Competing anchor | Own − competing |
| --- | --- | --- | --- | --- |
| Downstream files | 63.8% [58.9, 68.5] | 77.6% | 56.8% | +20.8 pp [15.2, 26.5] |
| Generated core files | 84.3% [77.0, 90.3] | 88.4% | 82.3% | +6.2 pp [2.1, 10.0] |

Percentile 95% CIs from a paired scenario-cluster bootstrap. Values are scenario-balanced over all 20 scenarios. `latest_finished` counts each run at its last finished attempt, after timeout retries; `first_finished` counts first attempts only.
