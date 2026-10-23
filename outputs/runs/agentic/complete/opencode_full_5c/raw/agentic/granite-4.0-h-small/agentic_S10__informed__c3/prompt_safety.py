import os
import json
from typing import Dict, Any, Optional

from model_client import CLIENT_MAP, validate_provider
from model_models import (
    build_extract_json_request,
    normalize_extract_json_output,
)

# ---------------------------------------------------------------------------
# Configuration\n# ---------------------------------------------------------------------------
DEFAULT_PROVIDER: str = os.getenv("DEFAULT_PROVIDER", "openai")
validate_provider(DEFAULT_PROVIDER)

# ---------------------------------------------------------------------------
# Public API\n# ---------------------------------------------------------------------------

def check_prompt_safety(prompt: str) -> Dict[str, Any]:
    """
    Evaluate a user prompt for unsafe or disallowed content.
    Returns a JSON‑compatible dict describing violations.
    """
    payload = build_extract_json_request(
        prompt,
        schema={"violations": []},
        model_provider=DEFAULT_PROVIDER,
        temperature=0.0,
        max_tokens=500,
    )
    raw = _call_provider(payload)
    return normalize_extract_json_output(raw) or {}

# ---------------------------------------------------------------------------
# Helper to invoke provider for moderation\n# ---------------------------------------------------------------------------
def _call_provider(payload: Dict[str, Any]) -> Any:
    # We reuse the generic extraction pipeline: the moderation model is treated
    # like any other LLM returning structured JSON.
    # Extract the moderation schema from model_client
    from model_client import CLIENT_MAP
    provider = payload["model_provider"]
    factory = CLIENT_MAP.get(provider)
    if not factory:
        raise ValueError(f"Unsupported provider: {provider}")
    client = factory()  # fresh client each call
    # Assuming the moderation model returns a field called 'content_flagged'
    # Adjust according to the real moderation model's output shape.
    response = client.chat_completions.create(
        **payload["messages"], **payload.get("kwargs", {})
    )
    return response

# ---------------------------------------------------------------------------
# CLI helper (optional)\n# ---------------------------------------------------------------------------
if __name__ == "__main__":
    if len(os.sys.argv) < 2:
        print("Usage: python prompt_safety.py <prompt_text>\")
        os.sys.exit(1)
    prompt = os.sys.argv[1]
    result = check_prompt_safety(prompt)
    print(json.dumps(result, indent=2, ensure_ascii=False))
