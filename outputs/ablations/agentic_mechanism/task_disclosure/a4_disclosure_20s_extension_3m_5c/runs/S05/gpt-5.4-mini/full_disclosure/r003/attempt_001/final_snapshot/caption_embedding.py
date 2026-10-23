import os
from typing import Iterable, List, Sequence

from openai import OpenAI


class CaptionEmbeddingError(RuntimeError):
    pass


def _client() -> OpenAI:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise CaptionEmbeddingError("OPENAI_API_KEY is required")
    return OpenAI(api_key=api_key)


def _chunk_texts(captions: Sequence[str]) -> List[str]:
    return [c.strip() for c in captions if c and c.strip()]


def embed_caption_chunks(caption_chunks: Iterable[str], model: str = "text-embedding-3-small") -> List[List[float]]:
    texts = _chunk_texts(list(caption_chunks))
    if not texts:
        return []
    client = _client()
    response = client.embeddings.create(model=model, input=texts)
    return [item.embedding for item in response.data]


def embed_caption_chunk(caption_chunk: str, model: str = "text-embedding-3-small") -> List[float]:
    embeddings = embed_caption_chunks([caption_chunk], model=model)
    return embeddings[0] if embeddings else []
