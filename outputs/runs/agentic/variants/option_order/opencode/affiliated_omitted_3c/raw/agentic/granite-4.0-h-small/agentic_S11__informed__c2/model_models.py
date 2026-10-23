import os
from typing import Any, Dict, TypedDict

# Concrete provider identifier used for response normalization
PROVIDER: str = "huggingface"


class NormalizedOutput(TypedDict):
    content: str
    usage: Dict[str, Any]


class RawProviderResponse(TypedDict):
    text: str
    generated_prompt: str
    usage: Dict[str, Any]


def normalize_response(raw: RawProviderResponse) -> NormalizedOutput:
    """Convert a provider‑specific raw response into a normalized shape.

    This helper makes downstream steps (safety, translation, embeddings, TTS)
    independent of the concrete provider.
    """
    # Example: Hugging Face response normalization
    return NormalizedOutput(
        content=raw["text"],
        usage=raw.get("usage", {}),
    )
