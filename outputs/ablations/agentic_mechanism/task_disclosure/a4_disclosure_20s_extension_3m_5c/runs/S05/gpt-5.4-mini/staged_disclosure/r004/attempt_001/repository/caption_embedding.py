import os
from typing import Iterable, List, Sequence

from openai import OpenAI


OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")


def _client() -> OpenAI:
    return OpenAI(api_key=os.environ["OPENAI_API_KEY"])


def embed_caption_chunks(chunks: Sequence[str]) -> List[List[float]]:
    texts = [chunk.strip() for chunk in chunks if chunk and chunk.strip()]
    if not texts:
        return []
    response = _client().embeddings.create(model=OPENAI_EMBEDDING_MODEL, input=texts)
    return [item.embedding for item in response.data]


def embed_caption_chunk(chunk: str) -> List[float]:
    embeddings = embed_caption_chunks([chunk])
    return embeddings[0] if embeddings else []


def semantic_search_query_embedding(query: str) -> List[float]:
    return embed_caption_chunk(query)
