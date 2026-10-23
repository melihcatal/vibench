#!/usr/bin/env python3
"""Print the runnable subset of a config's model list, skipping models
whose credentials are not configured.

Used by the smoke-test Makefile targets so smoke runs skip models with
missing API keys (or missing base URLs) instead of erroring. Reads
configs/.env the same way the generation runners do, overlaid on the
process environment. With --require-opencode, additionally requires an
"opencode" config object on the model entry (OpenCode runtime).

Output: runnable model IDs on one line (stdout); skip reasons on stderr.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
MODELS_JSON = BASE_DIR / "benchmark" / "vibench" / "models.json"
ENV_FILE = BASE_DIR / "configs" / ".env"


def load_env() -> dict[str, str]:
    env = dict(os.environ)
    if ENV_FILE.exists():
        for line in ENV_FILE.read_text().splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            key, value = key.strip(), value.strip().strip('"').strip("'")
            if value and key not in os.environ:
                env[key] = value
    return env


def config_models(config_path: Path) -> list[str]:
    import yaml

    with open(config_path) as f:
        config = yaml.safe_load(f)
    models = config.get("models")
    if not isinstance(models, list):
        raise SystemExit(f"{config_path} has no explicit models list")
    return models


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--config", type=Path,
                        default=BASE_DIR / "configs" / "vibench" / "direct" / "complete" / "full_5c.yaml")
    parser.add_argument("--require-opencode", action="store_true",
                        help="Only include models with an 'opencode' config object")
    args = parser.parse_args()

    registry = {m["id"]: m for m in json.loads(MODELS_JSON.read_text())["models"]}
    env = load_env()

    runnable = []
    for model_id in config_models(args.config):
        entry = registry.get(model_id)
        if entry is None:
            print(f"SKIP {model_id}: not registered in models.json", file=sys.stderr)
            continue
        missing = [var for var in (entry.get("api_key_env"), entry.get("api_base_env"))
                   if var and not env.get(var)]
        if missing:
            print(f"SKIP {model_id}: {', '.join(missing)} not set", file=sys.stderr)
            continue
        if args.require_opencode and not entry.get("opencode"):
            print(f"SKIP {model_id}: no 'opencode' config in models.json", file=sys.stderr)
            continue
        runnable.append(model_id)

    if not runnable:
        print("No runnable models (all skipped).", file=sys.stderr)
        raise SystemExit(1)
    print(" ".join(runnable))


if __name__ == "__main__":
    main()
