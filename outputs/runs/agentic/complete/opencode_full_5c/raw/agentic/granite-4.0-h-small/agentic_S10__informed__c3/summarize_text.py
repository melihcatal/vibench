import json
import os
from pathlib import Path
from typing import Optional

from model_client import CLIENT_MAP, validate_provider
from model_models import (
    build_summarize_text_request,
    normalize_summarize_output,
)

# ---------------------------------------------------------------------------
# Configuration (populate via environment variables)
# ---------------------------------------------------------------------------
# Example: export MISTRAL_API_KEY="sk-..." or set directly in code for testing
# The same environment variables are used in model_client.py

# Select which hosted model to call (case‑insensitive key from CLIENT_MAP)
# If not set, defaults to the most common provider (OpenAI)
DEFAULT_PROVIDER: str = os.getenv(
    "DEFAULT_PROVIDER",  # prioritized
    "openai",  # fallback if env not defined
)
validate_provider(DEFAULT_PROVIDER)  # will raise if required env vars missing

# ---------------------------------------------------------------------------
# Public API: summarize_text\n# ---------------------------------------------------------------------------


def summarize_text(
    long_text: str,
    provider: Optional[str] = None,
    **kwargs: dict,
) -> str:
    """
    Summarize arbitrary long text using a hosted LLM.

    Args:
        long_text: the document to summarize
        provider: optional key for the hosted model; uses DEFAULT_PROVIDER if None.
        **kwargs: forwarded to the provider’s SDK/REST client (e.g., temperature).

    Returns:
        Concise summary as a plain string.
    """
    provider = provider or DEFAULT_PROVIDER
    provider = provider.lower()
    payload = build_summarize_text_request(long_text, model_provider=provider, **kwargs)
    raw_response = _call_provider(provider, payload)
    return normalize_summarize_output(raw_response)


def _call_provider(provider_key: str, payload: dict) -> Any:
    """Generic wrapper to invoke the selected provider."""
    from model_client import CLIENT_MAP

    factory = CLIENT_MAP.get(provider_key)
    if not factory:
        raise ValueError(f"Unsupported provider: {provider_key}")
    # Get a fresh client each call to avoid state leakage
    client = factory()
    # Most SDKs expose a `chat_completions.create` style method
    return client.chat_completions.create(**payload)


# ---------------------------------------------------------------------------
# CLI entry point (optional, for quick manual testing)\n# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # Simple read‑file‑summarize demo
    if len(os.sys.argv) < 2:
        print(
            "Usage: python summarize_text.py <path_to_text> [--provider <key>] [--temperature <float>]"
        )
        os.sys.exit(1)
    text_path = Path(os.sys.argv[1]).expanduser()
    if not text_path.is_file():
        print(f"File not found: {text_path}")
        os.sys.exit(1)
    text = text_path.read_text(encoding="utf-8")
    provider = kwargs_provider = None
    args = os.sys.argv[2:]
    i = 0
    while i < len(args):
        if args[i] == "--provider":
            provider = args[i + 1]
            i += 2
            continue
        if args[i] == "--temperature":
            kwargs_provider = {"temperature": float(args[i + 1])}
            i += 2
            continue
        i += 1
    summary = summarize_text(text, provider=provider, **(kwargs_provider or {}))
    print("--- Summary ---")
    print(summary)
