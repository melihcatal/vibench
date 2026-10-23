from __future__ import annotations

from typing import Any, Dict, List

from model_client import OPENAI_DEFAULT_EMBEDDING_MODEL, get_openai_client


def platform_output_embedding(text: str) -> Dict[str, Any]:
    client = get_openai_client()
    response = client.embeddings.create(
        model=OPENAI_DEFAULT_EMBEDDING_MODEL,
        input=text,
    )
    embedding: List[float] = response.data[0].embedding
    return {
        "provider": "openai",
        "model": OPENAI_DEFAULT_EMBEDDING_MODEL,
        "embedding": embedding,
        "dimensions": len(embedding),
        "raw_response": response,
    }
