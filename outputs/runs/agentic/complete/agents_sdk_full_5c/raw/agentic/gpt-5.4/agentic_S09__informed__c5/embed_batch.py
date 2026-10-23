from __future__ import annotations

from collections.abc import Sequence

from embeddings_client import CohereEmbeddingsClient
from embeddings_models import normalize_embedding


def generate_batch_embeddings(
    texts: Sequence[str],
    *,
    input_type: str = "search_document",
    normalize: bool = False,
) -> list[list[float]]:
    client = CohereEmbeddingsClient()
    result = client.embed_texts(texts, input_type=input_type)
    if not normalize:
        return result.embeddings
    return [normalize_embedding(vector) for vector in result.embeddings]
