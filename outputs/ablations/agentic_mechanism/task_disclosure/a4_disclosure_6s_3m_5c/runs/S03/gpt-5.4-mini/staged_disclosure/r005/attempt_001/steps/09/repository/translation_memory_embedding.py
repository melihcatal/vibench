import os
from typing import Iterable, List, Sequence

from openai import OpenAI


OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")


def _client() -> OpenAI:
    return OpenAI(api_key=os.environ["OPENAI_API_KEY"])


def embed_segment(segment: str) -> List[float]:
    if not isinstance(segment, str) or not segment.strip():
        raise ValueError("segment must be a non-empty string")
    response = _client().embeddings.create(model=OPENAI_EMBEDDING_MODEL, input=segment)
    return list(response.data[0].embedding)


def embed_segments(segments: Sequence[str]) -> List[List[float]]:
    if not segments:
        return []
    normalized = []
    for segment in segments:
        if not isinstance(segment, str) or not segment.strip():
            raise ValueError("all segments must be non-empty strings")
        normalized.append(segment)
    response = _client().embeddings.create(model=OPENAI_EMBEDDING_MODEL, input=normalized)
    return [list(item.embedding) for item in response.data]


def embed_translation_memory(records: Iterable[dict]) -> List[dict]:
    prepared = []
    segments = []
    for record in records:
        if not isinstance(record, dict):
            raise ValueError("each record must be a dictionary")
        segment = record.get("translated_segment")
        if not isinstance(segment, str) or not segment.strip():
            raise ValueError("each record must include a non-empty translated_segment")
        prepared.append(record)
        segments.append(segment)
    embeddings = embed_segments(segments)
    return [
        {**record, "embedding": embedding}
        for record, embedding in zip(prepared, embeddings)
    ]
