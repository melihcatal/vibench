# Provider-option order (paper Tables 10-11)

**Concern.** The Reference-Open prompts list candidate providers. Selection
could be an artifact of where the affiliated provider sits in that list.

**Why.** Re-run the Reference-Open setting with the affiliated option placed
first, in the middle, last, and omitted entirely, in both the direct and
agentic settings.

**Result.** Reordering does not eliminate affiliated selection: the rate stays
in the 20-50% range wherever the affiliated option sits, and the pooled
First-Last contrast is not significant (-3.3 pp, 95% CI [-7.4, +0.8]).
Individual models do shift with position, in both directions. Omitting the
option drops every model below 2%. See [`headline.md`](headline.md).

**Where.** Configs ship in
`code/configs/vibench/direct/variants/option_order/` and
`code/configs/vibench/agentic/variants/option_order/` (four direct
placements; four OpenCode and two Agents SDK agentic placements). The appendix
table is built by
`code/scripts/evaluation/tables/generate_reference_order_appendix_table.py`.

This directory holds the appendix table and the headline summary. Rebuild them by
running the script above, then
`python ablations/snapshots/make_paper_summaries.py`.
