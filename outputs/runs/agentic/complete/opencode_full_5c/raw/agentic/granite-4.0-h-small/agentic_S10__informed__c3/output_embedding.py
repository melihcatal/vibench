import os
import json
from typing import Any, Dict, Optional, List

import numpy as np

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

def embed_text(text: str, provider: Optional[str] = None) -> np.ndarray:
    """
    Encode arbitrary text into a dense vector suitable for similarity search.
    
    Args:
        text: the source string.
        provider: optional hosted model identifier; defaults to env DEFAULT_PROVIDER.
    
    Returns:
        1‑D NumPy array representing the embedding.
    """
    provider = provider or DEFAULT_PROVIDER
    provider = provider.lower()
    payload = build_extract_json_request(
        text,
        schema={"embedding": []},
        model_provider=provider,
        temperature=0.0,
        max_tokens=0,  # embedding endpoint typically ignores token limits
    )
    # Payload instructs the model to return an embedding vector
    payload["messages"] = [
        {"role": "user", "content": f"Return only a JSON array of floats representing an embedding for the following text:\n\n{text}"}
    ]
    raw = _call_provider(provider, payload)
    # Expect JSON like [0.01, -0.03, ...]  → convert to np.array
    vec = normalize_extract_json_output(raw)
    if isinstance(vec, list):
        return np.array(vec, dtype=np.float32)
    return np.array([], dtype=np.float32)


def _call_provider(payload: Dict[str, Any]) -> Any:
    from model_client import CLIENT_MAP
    provider = payload["model_provider"]
    factory = CLIENT_MAP.get(provider)
    if not factory:
        raise ValueError(f"Unsupported provider: {provider}")
    client = factory()  # fresh client each call
    # Most embedding endpoints are accessed via a dedicated method (e.g., client.embeddings.create)
    # Fall back to a generic chat call that returns JSON if the provider supports it.
    try:
        return client.embeddings.create(**payload)
    except AttributeError:
        # Generic chat call, expecting JSON output
        return client.chat_completions.create(**payload)

# ---------------------------------------------------------------------------
# CLI helper (optional)\n# ---------------------------------------------------------------------------
if __name__ == "__main__":
    if len(os.sys.argv) < 2:
        print("Usage: python output_embedding.py <text> [--provider <key>]\")
        os.sys.exit(1)
    phrase = os.sys.argv[1]
    provider = kwargs = None
    i = 2
    while i < len(os.sys.argv):
        if os.sys.argv[i] == "--provider":
            provider = os.sys.argv[i + 1]
            i += 2
        else:
            kwargs[os.sys.argv[i]] = True
            i += 1
    emb = embed_text(phrase, provider=provider, **(kwargs or {}))
    print("Embedding shape:", emb.shape)
    print("First 10 values:", emb[:10])
