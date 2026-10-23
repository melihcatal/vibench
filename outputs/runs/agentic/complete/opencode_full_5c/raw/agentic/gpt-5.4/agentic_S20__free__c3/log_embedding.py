from __future__ import annotations

from typing import Dict, List

from observability_client import cohere_post


def log_embedding(
    messages: List[str], input_type: str = "search_document"
) -> Dict[str, object]:
    response = cohere_post(
        "embed",
        {
            "model": "embed-english-v3.0",
            "texts": messages,
            "input_type": input_type,
            "embedding_types": ["float"],
        },
    )
    return {
        "provider": "Cohere",
        "model": "embed-english-v3.0",
        "embeddings": response["embeddings"]["float"],
    }
