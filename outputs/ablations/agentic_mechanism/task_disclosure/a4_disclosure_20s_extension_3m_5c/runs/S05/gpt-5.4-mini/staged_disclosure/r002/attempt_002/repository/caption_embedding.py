import os
from typing import Iterable, List

from openai import OpenAI


OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"


def _client() -> OpenAI:
    return OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def _chunk_texts(caption_chunks: Iterable[str]) -> List[str]:
    return [chunk.strip() for chunk in caption_chunks if chunk and chunk.strip()]


def embed_caption_chunks(caption_chunks: Iterable[str]) -> List[List[float]]:
    texts = _chunk_texts(caption_chunks)
    if not texts:
        return []
    response = _client().embeddings.create(model=OPENAI_EMBEDDING_MODEL, input=texts)
    return [item.embedding for item in response.data]


def embed_caption_query(query: str) -> List[float]:
    text = query.strip()
    if not text:
        return []
    response = _client().embeddings.create(model=OPENAI_EMBEDDING_MODEL, input=text)
    return response.data[0].embedding
