import os
from typing import Iterable, List, Sequence

from openai import OpenAI


DEFAULT_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")


def _client() -> OpenAI:
    return OpenAI(api_key=os.environ["OPENAI_API_KEY"])


def embed_caption_chunks(chunks: Sequence[str], model: str = DEFAULT_MODEL) -> List[List[float]]:
    cleaned = [chunk.strip() for chunk in chunks if chunk and chunk.strip()]
    if not cleaned:
        return []
    response = _client().embeddings.create(model=model, input=cleaned)
    return [item.embedding for item in response.data]


def embed_single_caption_chunk(chunk: str, model: str = DEFAULT_MODEL) -> List[float]:
    embeddings = embed_caption_chunks([chunk], model=model)
    return embeddings[0] if embeddings else []


def embed_caption_iterable(chunks: Iterable[str], model: str = DEFAULT_MODEL) -> List[List[float]]:
    return embed_caption_chunks(list(chunks), model=model)
