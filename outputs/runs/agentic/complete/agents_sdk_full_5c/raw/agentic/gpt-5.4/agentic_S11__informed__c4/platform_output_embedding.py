from __future__ import annotations

from typing import Any, Dict, List

import cohere


DEFAULT_EMBED_MODEL = "embed-english-v3.0"


def platform_output_embedding(text: str, model: str = DEFAULT_EMBED_MODEL) -> Dict[str, Any]:
    client = cohere.ClientV2(api_key=__import__("os").environ["COHERE_API_KEY"])
    response = client.embed(
        model=model,
        input_type="search_document",
        texts=[text],
        embedding_types=["float"],
    )
    embeddings: List[float] = response.embeddings.float_[0]
    return {
        "provider": "Cohere",
        "model": model,
        "embedding": embeddings,
        "dimensions": len(embeddings),
        "raw_response": response,
    }
