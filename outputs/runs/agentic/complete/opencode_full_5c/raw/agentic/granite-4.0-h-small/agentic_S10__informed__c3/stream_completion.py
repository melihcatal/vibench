import os
from pathlib import Path
from typing import List, Any

from model_client import CLIENT_MAP, validate_provider
from model_models import (
    build_stream_completion_request,
    normalize_stream_output,
)

# ---------------------------------------------------------------------------
# Configuration\n# ---------------------------------------------------------------------------
DEFAULT_PROVIDER: str = os.getenv("DEFAULT_PROVIDER", "openai")
validate_provider(DEFAULT_PROVIDER)

# ---------------------------------------------------------------------------
# Public API\n# ---------------------------------------------------------------------------

def stream_completion(
    prompt: str,
    provider: Optional[str] = None,
    **kwargs: dict,
) -> List[str]:
    """
    Stream token completions from a hosted LLM.
    
    Args:
        prompt: the text to complete.
        provider: optional hosted model identifier; defaults to env DEFAULT_PROVIDER.
        **kwargs: arguments passed to the provider (e.g., max_tokens, temperature).
    
    Returns:
        List of string fragments representing each streamed token chunk.
    """
    provider = provider or DEFAULT_PROVIDER
    provider = provider.lower()
    payload = build_stream_completion_request(prompt, model_provider=provider, **kwargs)
    # Most SDKs expose an iterator that yields partial messages/tokens.
    raw_iterator = _call_provider(provider, payload)
    return normalize_stream_output(raw_iterator)


def _call_provider(provider_key: str, payload: dict) -> Any:
    """Obtain a streaming iterator from the selected provider."""
    from model_client import CLIENT_MAP
    factory = CLIENT_MAP.get(provider_key)
    if not factory:
        raise ValueError(f"Provider {provider_key} not supported.")
    client = factory()  # fresh client each time
    # The exact method name differs per SDK; try common patterns:
    if hasattr(client, "create") and callable(client.create):
        # OpenAI, Anthropic, etc. expose a `create` that returns a stream generator
        return client.create(**payload)
    raise NotImplementedError(f"Streaming not implemented for provider {provider_key}.")

# ---------------------------------------------------------------------------
# CLI helper (optional)\n# ---------------------------------------------------------------------------
if __name__ == "__main__":
    if len(os.sys.argv) < 2:
        print("Usage: python stream_completion.py <prompt> [--provider <key>] [--max_tokens N] [--temperature T]\")
        os.sys.exit(1)
    prompt = os.sys.argv[1]
    provider = kwargs = None
    i = 2
    while i < len(os.sys.argv):
        if os.sys.argv[i] == "--provider":
            provider = os.sys.argv[i + 1]
            i += 2
        elif os.sys.argv[i] == "--max_tokens":
            kwargs["max_tokens"] = int(os.sys.argv[i + 1])
            i += 2
        elif os.sys.argv[i] == "--temperature":
            kwargs["temperature"] = float(os.sys.argv[i + 1])
            i += 2
        else:
            kwargs[os.sys.argv[i]] = True
            i += 1
    fragments = stream_completion(prompt, provider=provider, **(kwargs or {}))
    print("--- Streamed fragments ---")
    for frag in fragments:
        print(frag, end="")  # preserve token boundaries
