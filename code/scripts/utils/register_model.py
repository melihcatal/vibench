#!/usr/bin/env python3
"""Register a model in benchmark/vibench/models.json.

One JSON entry is all a new model needs to flow through generation,
evaluation, tables, and plots (the model registry supplies defaults
everywhere else). Typical use, followed by a single-model evaluation
against a published control baseline:

    python scripts/utils/register_model.py \
        --id mai-thinking-1 \
        --litellm-string azure_ai/mai-thinking-1 \
        --api-key-env AZURE_AI_API_KEY \
        --ecosystem microsoft_openai \
        --role affiliated --tier flagship \
        --developer "Microsoft AI"

    make eval-model MODEL=mai-thinking-1

Models registered here do NOT get a study_order: they never join the
frozen study grid (or its control baseline) implicitly.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
MODELS_JSON = BASE_DIR / "benchmark" / "vibench" / "models.json"

EVAL_DIR = BASE_DIR / "scripts" / "evaluation"
# The evaluation modules form one namespace, grouped into folders for readability.
for _group in ("core", "gini", "tables", "baselines", "audit"):
    if str(EVAL_DIR / _group) not in sys.path:
        sys.path.insert(0, str(EVAL_DIR / _group))

import model_registry as registry  # noqa: E402

KNOWN_ECOSYSTEMS = {"google", "microsoft_openai", "aws", "ibm", "alibaba"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--id", required=True, help="Model ID used in runs and reports")
    parser.add_argument("--litellm-string", required=True, help="LiteLLM route, e.g. gemini/gemini-2.5-flash")
    parser.add_argument("--api-key-env", required=True, help="Environment variable holding the API key")
    parser.add_argument("--role", choices=["affiliated", "independent", "control"], required=True)
    parser.add_argument("--ecosystem", default=None,
                        help=f"Ecosystem affiliation (required for role=affiliated); known: {sorted(KNOWN_ECOSYSTEMS)}")
    parser.add_argument("--tier", choices=["flagship", "budget"], default="flagship")
    parser.add_argument("--display-name", default=None, help="Defaults to the model ID")
    parser.add_argument("--developer", default=None)
    parser.add_argument("--api-provider", default=None)
    parser.add_argument("--provider-family", default=None, help="Defaults to the ecosystem (or developer)")
    parser.add_argument("--note", default=None, help="Optional affiliation/litellm note")
    parser.add_argument("--dry-run", action="store_true", help="Print the entry without writing models.json")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.role == "affiliated" and not args.ecosystem:
        raise SystemExit("--ecosystem is required for role=affiliated")
    if args.ecosystem and args.ecosystem not in KNOWN_ECOSYSTEMS:
        print(f"WARNING: ecosystem '{args.ecosystem}' is not among the known ecosystems "
              f"{sorted(KNOWN_ECOSYSTEMS)}; the detector must know how to attribute it.")
    if args.id in registry.models_info():
        raise SystemExit(f"Model '{args.id}' is already registered")

    entry = {
        "id": args.id,
        "display_name": args.display_name or args.id,
        "developer": args.developer,
        "litellm_string": args.litellm_string,
        "api_provider": args.api_provider,
        "api_key_env": args.api_key_env,
        "provider_family": args.provider_family or args.ecosystem or (args.developer or "").lower() or None,
        "direct_provider_affiliation": args.ecosystem,
        "ecosystem_affiliation": args.ecosystem if args.role == "affiliated" else None,
        "cloud_affiliation": args.ecosystem if args.role == "affiliated" else None,
        "affiliation_type": "direct_ownership" if args.role == "affiliated" else args.role,
        "tier": args.tier,
        "role": args.role,
        "default_temperature": 1.0,
    }
    if args.note:
        entry["litellm_note"] = args.note
    entry = {k: v for k, v in entry.items() if v is not None}

    if args.dry_run:
        print(json.dumps(entry, indent=2))
        return

    data = json.loads(MODELS_JSON.read_text())
    data["models"].append(entry)
    MODELS_JSON.write_text(json.dumps(data, indent=2) + "\n")
    print(f"Registered '{args.id}' ({args.role}, {entry.get('ecosystem_affiliation') or 'no ecosystem'}). "
          f"Next: make eval-model MODEL={args.id}")


if __name__ == "__main__":
    main()
