# Assigned initial provider — results

Derived from `ablations/snapshots/a1_a3_retry_snapshot_20260921_finished/bootstrap_results.json` by `ablations/snapshots/make_summaries.py`.

Paired scenario-cluster percentile bootstrap; fixed models; no within-scenario resampling. 10000 replicates, seed 20260921.

## Attempt scope: `latest_finished` (reported in the paper)

| File set | Anchor followed (all anchors) | Own-ecosystem anchor | Competing anchor | Own − competing |
| --- | --- | --- | --- | --- |
| Downstream files | 59.6% [53.7, 65.4] | 78.2% | 50.2% | +28.0 pp [21.9, 34.2] |
| Generated core files | 84.7% [79.2, 89.1] | 88.6% | 82.8% | +5.8 pp [2.0, 9.6] |

## Attempt scope: `first_finished`

| File set | Anchor followed (all anchors) | Own-ecosystem anchor | Competing anchor | Own − competing |
| --- | --- | --- | --- | --- |
| Downstream files | 58.6% [52.7, 64.4] | 78.0% | 48.9% | +29.1 pp [22.9, 35.4] |
| Generated core files | 83.7% [78.2, 88.1] | 88.3% | 81.4% | +6.8 pp [2.2, 11.3] |

Percentile 95% CIs from a paired scenario-cluster bootstrap. Values are scenario-balanced over all 20 scenarios. `latest_finished` counts each run at its last finished attempt, after timeout retries; `first_finished` counts first attempts only.
