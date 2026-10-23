from __future__ import annotations

from typing import Iterable, List

from model_client import DEFAULT_OPENAI_EMBEDDING_MODEL, build_client
from model_models import EmbeddingResult


def embed_outputs(texts: Iterable[str], model: str = DEFAULT_OPENAI_EMBEDDING_MODEL) -> EmbeddingResult:
    text_list: List[str] = list(texts)
    client = build_client().client
    response = client.embeddings.create(
        model=model,
        input=text_list,
    )
    vectors = [item.embedding for item in response.data]
    return EmbeddingResult(
        provider="openai",
        model=model,
        embeddings=vectors,
        raw=response,
    )
