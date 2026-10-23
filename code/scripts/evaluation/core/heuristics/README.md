# Provider-attribution heuristics

The rules the detector matches against generated code, kept as data so they can
be read, audited and extended without touching detection logic. `detect_services.py`
loads these at import; nothing else reads them.

| File | Entries | What it is |
|---|---:|---|
| `detection_rules.json` | 224 | ordered `[pattern, service, provider]` rules |
| `provider_ecosystem.json` | 50 | provider → ecosystem VIB aggregates over |
| `sdk_hints.json` | 13 | per-provider first-party SDK patterns |
| `rest_hints.json` | 13 | per-provider REST-endpoint patterns |

Each file is `{"_doc": "...", "data": ...}`; the detector reads `data`.

## detection_rules.json

```json
["google\\.cloud\\.pubsub|PublisherClient|topic_path\\(\\)", "Google Cloud Pub/Sub", "google"]
```

- **pattern** — a Python regex matched against the generated source after Python
  line comments are stripped. Escape backslashes for JSON.
- **service** — the human-readable name recorded on a match, and what appears in
  the per-file detail of an evaluation report.
- **provider** — what the match attributes to. Must be a key in
  `provider_ecosystem.json`, or the literal `independent` for a library that
  implies no provider.

**Order matters.** The list is evaluated top to bottom and the first match wins,
so specific rules precede generic ones: the `google\.cloud\.pubsub` rule sits
above the bare `google` catch-all, and `independent` wrapper libraries such as
`googletrans` sit above anything that would otherwise claim them for Google.

## Extending them

Adding a provider or service means adding a rule, and if the provider is new,
an entry in `provider_ecosystem.json`. Insert the rule **above** any generic
rule that would shadow it, then re-run detection and compare:

```bash
cd code
python scripts/evaluation/core/detect_services.py --run direct/complete/full_5c
make evaluate
```

A rule that changes any existing attribution will show up as a different
detection rate or a changed per-model ecosystem share, so diff the report
before and after.

## Why they are data

Provider attribution is the step the metric rests on: VIB is the difference
between an affiliated model's ecosystem share and the controls' on the same
task, so a mis-attribution moves the result. Keeping the rules inspectable
means a reader can check what the detector counts as "Google Cloud Pub/Sub"
without reading 700 lines of matching code, and the 400-sample human audit
(`code/benchmark/vibench/audit/`) can be re-run against a modified rule set.

The detector reports a confidence and a detection method per file — `sdk`,
`sdk_and_rest`, `rest_endpoint`, `keyword_or_env_only`, `cs_option_match` — so
a match driven only by an environment-variable name is distinguishable from one
backed by a first-party SDK import. Those classifications come from
`sdk_hints.json` and `rest_hints.json`.
