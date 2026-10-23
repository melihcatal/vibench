import os
from typing import Iterable, List

from openai import OpenAI


EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")


def _normalize_caption_chunk(chunk: object) -> str:
    if chunk is None:
        return ""
    if isinstance(chunk, str):
        return chunk.strip()
    if isinstance(chunk, dict):
        for key in ("text", "caption", "content", "chunk"):
            value = chunk.get(key)
            if isinstance(value, str) and value.strip():
                return value.strip()
        return " ".join(str(v).strip() for v in chunk.values() if isinstance(v, str) and v.strip())
    return str(chunk).strip()


def embed_caption_chunks(chunks: Iterable[object]) -> List[List[float]]:
    texts = [_normalize_caption_chunk(chunk) for chunk in chunks]
    texts = [text for text in texts if text]
    if not texts:
        return []
    client = OpenAI()
    response = client.embeddings.create(model=EMBEDDING_MODEL, input=texts)
    return [item.embedding for item in response.data]
