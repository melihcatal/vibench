from __future__ import annotations

from typing import List

from vertexai.language_models import TextEmbeddingModel

from model_client import init_vertex_ai


EMBEDDING_MODEL_ID = "text-embedding-004"


def embed_platform_output(text: str) -> List[float]:
    init_vertex_ai()
    model = TextEmbeddingModel.from_pretrained(EMBEDDING_MODEL_ID)
    result = model.get_embeddings([text])[0]
    return list(result.values)
