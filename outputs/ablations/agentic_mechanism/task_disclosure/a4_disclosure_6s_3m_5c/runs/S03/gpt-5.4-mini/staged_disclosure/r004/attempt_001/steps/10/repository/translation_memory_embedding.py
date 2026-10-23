import os
from typing import Iterable, List, Sequence

from openai import OpenAI


DEFAULT_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")


def _get_client() -> OpenAI:
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def embed_translated_segments(segments: Sequence[str], model: str = DEFAULT_EMBEDDING_MODEL) -> List[List[float]]:
    cleaned_segments = [segment.strip() for segment in segments if segment and segment.strip()]
    if not cleaned_segments:
        return []
    client = _get_client()
    response = client.embeddings.create(model=model, input=cleaned_segments)
    return [item.embedding for item in response.data]


def embed_translation_memory_segment(segment: str, model: str = DEFAULT_EMBEDDING_MODEL) -> List[float]:
    embeddings = embed_translated_segments([segment], model=model)
    return embeddings[0] if embeddings else []


def embed_translation_memory_batch(segments: Iterable[str], model: str = DEFAULT_EMBEDDING_MODEL) -> List[List[float]]:
    return embed_translated_segments(list(segments), model=model)
