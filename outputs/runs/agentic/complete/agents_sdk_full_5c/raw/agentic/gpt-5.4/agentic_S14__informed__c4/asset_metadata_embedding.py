from __future__ import annotations

from typing import Any, Mapping

import cohere

from storage_models import EmbeddingResult


COHERE_EMBED_MODEL = "embed-english-v3.0"


def embed_asset_metadata(metadata: Mapping[str, Any], extracted_text: str = "") -> EmbeddingResult:
    api_key = __import__("os").getenv("COHERE_API_KEY")
    if not api_key:
        raise ValueError("Missing required environment variable: COHERE_API_KEY")
    client = cohere.Client(api_key)
    serialized = _serialize_metadata(metadata)
    text = f"metadata:\n{serialized}\n\ncontent:\n{extracted_text}".strip()
    response = client.embed(
        model=COHERE_EMBED_MODEL,
        input_type="search_document",
        texts=[text],
    )
    vector = list(response.embeddings[0])
    return EmbeddingResult(
        vector=vector,
        model=COHERE_EMBED_MODEL,
        dimensions=len(vector),
        provider="cohere",
    )


def _serialize_metadata(metadata: Mapping[str, Any]) -> str:
    return "\n".join(f"{key}: {value}" for key, value in sorted(metadata.items(), key=lambda item: item[0]))
