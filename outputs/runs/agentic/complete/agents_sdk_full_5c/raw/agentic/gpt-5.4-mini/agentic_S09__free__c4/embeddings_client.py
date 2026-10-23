import os
from functools import lru_cache
from typing import Optional

from openai import OpenAI

from embeddings_models import EmbeddingRequest

OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")


@lru_cache(maxsize=1)
def get_openai_client() -> OpenAI:
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def build_embedding_request(texts, model: Optional[str] = None, dimensions: Optional[int] = None) -> EmbeddingRequest:
    return EmbeddingRequest(texts=list(texts), model=model or OPENAI_EMBEDDING_MODEL, dimensions=dimensions)
