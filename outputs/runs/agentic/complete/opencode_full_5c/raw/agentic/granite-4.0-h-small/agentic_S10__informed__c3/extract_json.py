import json
import os
from pathlib import Path
from typing import Any, Dict, Optional

from model_client import CLIENT_MAP, validate_provider
from model_models import (
    build_extract_json_request,
    normalize_extract_json_output,
)

# ---------------------------------------------------------------------------
# Configuration\n# ---------------------------------------------------------------------------
# Same environment variables used in model_client.py
DEFAULT_PROVIDER: str = os.getenv("DEFAULT_PROVIDER", "openai")
validate_provider(DEFAULT_PROVIDER)

# ---------------------------------------------------------------------------
# Public API\n# ---------------------------------------------------------------------------

def extract_json(
    text: str,
    schema: Dict[str, Any],
    provider: Optional[str] = None,
    **kwargs: dict,
) -> Optional[Dict[str, Any]]:
    """
    Extract structured JSON from arbitrary text using a hosted LLM.
    
    Args:
        text: the source document.
        schema: a JSON Schema describing the desired output shape.
        provider: optional hosted model identifier; falls back to DEFAULT_PROVIDER.
        **kwargs: extra arguments passed to the provider (e.g., temperature).
    
    Returns:
        Parsed JSON object (dict) if extraction succeeded, else None.
    """
    provider = provider or DEFAULT_PROVIDER
    provider = provider.lower()
    payload = build_extract_json_request(text, schema, model_provider=provider, **kwargs)
    raw = _call_provider(provider, payload)
    return normalize_extract_json_output(raw)


def _call_provider(provider_key: str, payload: Dict[str, Any]) -> Any:
    """Dispatch to the concrete provider client."""
    from model_client import CLIENT_MAP
    factory = CLIENT_MAP.get(provider_key)
    if not factory:
        raise ValueError(f"Provider {provider_key} not configured.")
    client = factory()  # fresh client each call
    return client.chat_completions.create(**payload)

# ---------------------------------------------------------------------------
# CLI helper (optional)\n# ---------------------------------------------------------------------------
if __name__ == "__main__":
    if len(os.sys.argv) < 3:
        print("Usage: python extract_json.py <path_to_text> <path_to_schema_json> [--provider <key>]\")
        os.sys.exit(1)
    text_path = Path(os.sys.argv[1]).expanduser()
    schema_path = Path(os.sys.argv[2]).expanduser()
    provider = kwargs = None
    i = 3
    while i < len(os.sys.argv):
        if os.sys.argv[i] == "--provider":
            provider = os.sys.argv[i + 1]
            i += 2
        else:
            # treat remaining args as key=value pairs for kwargs
            if "=" in os.sys.argv[i]:
                k, v = os.sys.argv[i].split("=", 1)
                kwargs[k] = v
            else:
                # assume flag without value
                kwargs[os.sys.argv[i]] = True
            i += 1
    if not text_path.is_file():
        print(f"Text file not found: {text_path}")
        os.sys.exit(1)
    if not schema_path.is_file():
        print(f"Schema file not found: {schema_path}")
        os.sys.exit(1)
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    result = extract_json(text_path.read_text(encoding="utf-8"), schema, provider=provider, **(kwargs or {}))
    if result:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print("Extraction returned no JSON.")
