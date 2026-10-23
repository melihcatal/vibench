# Single-shot multi-file generation — results

Derived from `ablations/snapshots/20260919_full_a2_a3/results.json` by `ablations/snapshots/make_summaries.py`.

Share of task-aligned core files assigned to the model's affiliated ecosystem (`core`), over runs with extractable output.

| Model | Single-shot | Original agentic | Difference |
| --- | --- | --- | --- |
| `gemini-2.5-flash` | 43.2% [37.8, 48.6] | 79.0% [73.6, 84.1] | +35.8 pp |
| `gpt-5.4-mini` | 37.9% [32.5, 43.2] | 43.5% [40.2, 46.8] | +5.6 pp |
| `nova-pro` | 23.2% [19.6, 26.9] | 70.0% [65.0, 74.8] | +46.8 pp |

Difference is original agentic minus single-shot: a positive value means the affiliated share was higher with agent tools than in one response.

Conservative bound, keeping every run and scoring an unextractable one as zero (`all_assigned_core_missing_zero`):

| Model | Single-shot | Original agentic |
| --- | --- | --- |
| `gemini-2.5-flash` | 38.1% (91/100 runs extractable) | 79.0% (100/100) |
| `gpt-5.4-mini` | 37.9% (99/100 runs extractable) | 43.5% (100/100) |
| `nova-pro` | 21.0% (88/100 runs extractable) | 70.0% (100/100) |
