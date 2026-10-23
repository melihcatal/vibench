# Microsoft/OpenAI anchor extension

Adds only `anchor_microsoft_openai` to A1. Uses Gemini 2.5 Flash, GPT-5.4 Mini,
and Nova Pro, all 20 scenarios, five repetitions: 300 new runs. The per-repository
timeout is 300 seconds and sampling inherits the original paper YAMLs.

The supplied A1 uses the Microsoft/OpenAI evidence entry for each scenario.
S09/S10 use the public OpenAI API; S11 uses Azure OpenAI; the other scenarios use
Microsoft/Azure services. This is the paper's merged ecosystem, not an
OpenAI-only or direct-affiliation test. Report surface-specific results separately
if interpreting direct versus indirect affiliation.

The original archived NLI prompt receives only the same existing-file notice as
the Google/AWS conditions. Only the primary Python file is seeded into the agent
workspace; requirements, metadata, and evidence remain outside it. Generation,
provider attribution, missing-output denominators, progress and retry behavior
reuse the existing runner. Supplied A1 is excluded from generated-file scores.

## Validation and service differences

Templates pass syntax, provider-attribution and mocked request/response tests.
They have NOT been executed against live cloud services. They require provisioned
resources and credentials if actually invoked. Per-scenario metadata preserves
the evidence entry, package choices, and implementation preconditions.

- S04 uses [Azure Speech batch REST](https://learn.microsoft.com/en-us/azure/ai-services/speech-service/batch-transcription-create)
  rather than the bundle's synchronous SDK method, preserving asynchronous job submission.
- S17 uses an AES key in Managed HSM and returns IV/tag metadata needed for decryption.
- S19 pins `azure-monitor-query==1.4.1`, preserving the archived MetricsQueryClient
  interface [removed in version 2](https://learn.microsoft.com/en-us/python/api/overview/azure/monitor-query-readme?view=azure-python).
- S09/S10 follow the documented [embeddings](https://developers.openai.com/api/docs/guides/embeddings)
  and [chat-completions](https://developers.openai.com/api/reference/resources/chat/subresources/completions/methods/create) interfaces.
- Equivalent high-level tasks do not imply identical authentication, safety
  taxonomies, cryptographic serialization, latency, or output quality.

## Run

From the working repository root:

```bash
python -u -B ablations/initial_provider/assigned_as_code/microsoft_openai/scripts/run.py \
  --config ablations/initial_provider/assigned_as_code/microsoft_openai/config.yaml \
  --output ablations/outputs/a1_microsoft_openai_20s_3m_5c \
  --execute
```

Omit `--execute` for a dry run. Resume with `--resume`; add `--retry-failed` only
to request new attempts for failures. Old outputs are preserved. No Google/AWS
cells are scheduled. Run A3 separately after A1, not concurrently by default.

Extension scripts live in a separate directory so old campaign source hashes,
particularly the ongoing A4 run, remain unchanged. The new plan fingerprints its
extension scripts and prepared inputs. Do not edit them after starting.

To verify the prepared inputs and offline tests:

```bash
python -B ablations/initial_provider/assigned_as_code/microsoft_openai/scripts/build_inputs.py --check
python -B -m unittest discover -s ablations/initial_provider/assigned_as_code/microsoft_openai/tests -v
```

These additional collection waves are not contemporaneous with the completed
Google/AWS runs. Preserve collection times and failures when comparing them.
