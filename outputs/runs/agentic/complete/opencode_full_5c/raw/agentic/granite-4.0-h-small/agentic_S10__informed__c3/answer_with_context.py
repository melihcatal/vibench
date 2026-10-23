import json
import os
from pathlib import Path
from typing import Any, Dict, Optional

from model_client import CLIENT_MAP, validate_provider
from model_models import (
    build_answer_with_context_request,
    normalize_answer_output,
)

# ---------------------------------------------------------------------------
# Configuration\n# ---------------------------------------------------------------------------
DEFAULT_PROVIDER: str = os.getenv("DEFAULT_PROVIDER", "openai")
validate_provider(DEFAULT_PROVIDER)

# ---------------------------------------------------------------------------
# Public API\n# ---------------------------------------------------------------------------

def answer_with_context(
    question: str,
    context: str,
    provider: Optional[str] = None,
    **kwargs: dict,
) -> str:
    """
    Answer a natural‑language question using supplied background context.
    
    Args:
        question: user question.
        context: background material the model should consider.
        provider: optional hosted model identifier; uses DEFAULT_PROVIDER if omitted.
        **kwargs: arguments forwarded to the provider (e.g., temperature).
    
    Returns:
        Concise answer string.
    """
    provider = provider or DEFAULT_PROVIDER
    provider = provider.lower()
    payload = build_answer_with_context_request(question, context, model_provider=provider, **kwargs)
    raw = _call_provider(provider, payload)
    return normalize_answer_output(raw)


def _call_provider(provider_key: str, payload: Dict[str, Any]) -> Any:
    """Route to the concrete provider SDK."""
    from model_client import CLIENT_MAP
    factory = CLIENT_MAP.get(provider_key)
    if not factory:
        raise ValueError(f"Unsupported provider: {provider_key}")
    client = factory()  # fresh client each request
    return client.chat_completions.create(**payload)

# ---------------------------------------------------------------------------
# CLI helper (optional)\n# ---------------------------------------------------------------------------
if __name__ == "__main__":
    if len(os.sys.argv) < 3:
        print("Usage: python answer_with_context.py <question_text> <context_text> [--provider <key>]\")
        os.sys.exit(1)
    question = os.sys.argv[1]
    context = os.sys.argv[2]
    provider = kwargs = None
    i = 3
    while i < len(os.sys.argv):
        if os.sys.argv[i] == "--provider":
            provider = os.sys.argv[i + 1]
            i += 2
        else:
            kwargs[os.sys.argv[i]] = True
            i += 1
    answer = answer_with_context(question, context, provider=provider, **(kwargs or {}))
    print("--- Answer ---")
    print(answer)
