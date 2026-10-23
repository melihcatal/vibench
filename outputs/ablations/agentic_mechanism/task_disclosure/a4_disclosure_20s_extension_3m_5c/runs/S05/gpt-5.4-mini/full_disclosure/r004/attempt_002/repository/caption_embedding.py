import os
from typing import Iterable, List, Sequence

from openai import OpenAI


DEFAULT_EMBEDDING_MODEL = "text-embedding-3-small"


def _client() -> OpenAI:
    return OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def embed_caption_chunks(chunks: Sequence[str], model: str = DEFAULT_EMBEDDING_MODEL) -> List[List[float]]:
    texts = [chunk.strip() for chunk in chunks if chunk and chunk.strip()]
    if not texts:
        return []
    response = _client().embeddings.create(model=model, input=texts)
    return [item.embedding for item in response.data]


def embed_caption_chunk(chunk: str, model: str = DEFAULT_EMBEDDING_MODEL) -> List[float]:
    embeddings = embed_caption_chunks([chunk], model=model)
    return embeddings[0] if embeddings else []
