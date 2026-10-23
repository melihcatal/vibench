from __future__ import annotations

from typing import Iterable, List

from openai import OpenAI


OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"


def embed_caption_chunks(captions: Iterable[str]) -> List[List[float]]:
    client = OpenAI()
    texts = [caption.strip() for caption in captions if caption.strip()]
    if not texts:
        return []
    response = client.embeddings.create(model=OPENAI_EMBEDDING_MODEL, input=texts)
    return [item.embedding for item in response.data]
