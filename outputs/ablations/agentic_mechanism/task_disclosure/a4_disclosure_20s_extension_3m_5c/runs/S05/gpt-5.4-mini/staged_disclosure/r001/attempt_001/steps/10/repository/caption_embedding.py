import os
from typing import Iterable, List, Sequence

from openai import OpenAI


DEFAULT_EMBEDDING_MODEL = "text-embedding-3-small"


def _client() -> OpenAI:
    return OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def normalize_caption_chunks(caption_chunks: Iterable[str]) -> List[str]:
    return [chunk.strip() for chunk in caption_chunks if chunk and chunk.strip()]


def embed_caption_chunks(caption_chunks: Sequence[str], model: str = DEFAULT_EMBEDDING_MODEL) -> List[List[float]]:
    chunks = normalize_caption_chunks(caption_chunks)
    if not chunks:
        return []
    response = _client().embeddings.create(model=model, input=chunks)
    return [item.embedding for item in response.data]


def embed_single_caption_chunk(caption_chunk: str, model: str = DEFAULT_EMBEDDING_MODEL) -> List[float]:
    embeddings = embed_caption_chunks([caption_chunk], model=model)
    return embeddings[0] if embeddings else []
