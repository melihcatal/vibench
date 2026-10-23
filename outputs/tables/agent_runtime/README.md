# Agentic runtime comparison (paper Table 12)

**Concern.** The agentic results might be specific to one agent framework
rather than to agentic generation.

**Why.** Repeat the agentic arm on a second runtime. The main results use
OpenCode; this arm uses the OpenAI Agents SDK with the same benchmark tasks,
prompt construction, and sampling.

**Result.** The sign of VIB agrees on both runtimes for 6 of 7 affiliated
models, so the finding is not an artifact of one agent framework. Magnitudes
are generally smaller under the Agents SDK, which is why OpenCode is the main
arm and this is the robustness check. See
[`headline.md`](headline.md).

**Where.** `code/scripts/generation/run_agentic_litellm_agents.py` with
`code/configs/vibench/agentic/complete/agents_sdk_full_5c.yaml`. Run it with
`make gen-agents-sdk-full` from `code/`.

This directory holds both evaluator reports and the derived comparison. Rebuild
them with:

```bash
python scripts/evaluation/core/evaluate_agentic.py --run agentic/complete/opencode_full_5c   --direct-run direct/complete/full_5c
python scripts/evaluation/core/evaluate_agentic.py --run agentic/complete/agents_sdk_full_5c --direct-run direct/complete/full_5c
python ../ablations/snapshots/make_paper_summaries.py
```
