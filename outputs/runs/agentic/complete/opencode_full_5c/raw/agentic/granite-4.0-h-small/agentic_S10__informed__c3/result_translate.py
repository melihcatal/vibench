import os
import json
from typing import Any, Dict, Optional

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

def translate_text(
    text: str,
    target_language: str = "en",
    provider: Optional[str] = None,
    **kwargs: dict,
) -> str:
    """
    Translate arbitrary text into the target language using a hosted LLM.
    
    Args:
        text: source string.
        target_language: ISO language code (e.g., 'es', 'fr').
        provider: optional hosted model; defaults to env DEFAULT_PROVIDER.
        **kwargs: extra arguments for the provider (temperature, etc.).
    
    Returns:
        Translated string.
    """
    provider = provider or DEFAULT_PROVIDER
    provider = provider.lower()
    payload = build_extract_json_request(
        text,
        schema={"translation": ""},
        model_provider=provider,
        temperature=0.0,
        max_tokens=500,
        **kwargs,
    )
    # The prompt instructs the model to translate
    payload["messages"] = [
        {"role": "user", "content": f"Translate the following text into {target_language}:\n\n{text}"}
    ]
    raw = _call_provider(provider, payload)
    return normalize_extract_json_output(raw) or ""


def _call_provider(payload: Dict[str, Any]) -> Any:
    # Use generic extraction pipeline: the target LLM returns JSON with a 'translation' field.
    from model_client import CLIENT_MAP
    provider = payload["model_provider"]
    factory = CLIENT_MAP.get(provider)
    if not factory:
        raise ValueError(f"Unsupported provider: {provider}")
    client = factory()  # fresh client per request
    # Assume SDK provides chat completions; we extract the first message content.
    response = client.chat_completions.create(**payload)
    return response

# ---------------------------------------------------------------------------
# CLI helper (optional)\n# ---------------------------------------------------------------------------
if __name__ == "__main__":
    if len(os.sys.argv) < 3:
        print("Usage: python result_translate.py <text> <target_language> [--provider <key>]\")
        os.sys.exit(1)
    source = os.sys.argv[1]
    target = os.sys.argv[2]
    provider = kwargs = None
    i = 3
    while i < len(os.sys.argv):
        if os.sys.argv[i] == "--provider":
            provider = os.sys.argv[i + 1]
            i += 2
        else:
            kwargs[os.sys.argv[i]] = True
            i += 1
    translation = translate_text(source, target, provider=provider, **(kwargs or {}))
    print("--- Translation ---")
    print(translation)
