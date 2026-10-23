import os
from typing import Iterable, List, Sequence

from openai import OpenAI


DEFAULT_EMBEDDING_MODEL = "text-embedding-3-small"


def _normalize_segment(segment) -> str:
    if segment is None:
        return ""
    if isinstance(segment, str):
        return segment.strip()
    if isinstance(segment, dict):
        for key in ("text", "content", "segment", "transcript", "utterance"):
            value = segment.get(key)
            if isinstance(value, str) and value.strip():
                return value.strip()
        parts = []
        for key in ("speaker", "start", "end", "text"):
            value = segment.get(key)
            if value is not None:
                parts.append(str(value))
        return " ".join(parts).strip()
    return str(segment).strip()


def embed_transcript_segments(
    segments: Sequence[object],
    model: str = DEFAULT_EMBEDDING_MODEL,
    api_key: str | None = None,
) -> List[List[float]]:
    texts = [_normalize_segment(segment) for segment in segments]
    client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
    response = client.embeddings.create(model=model, input=texts)
    ordered = sorted(response.data, key=lambda item: item.index)
    return [item.embedding for item in ordered]


def embed_transcript_segment(segment: object, model: str = DEFAULT_EMBEDDING_MODEL, api_key: str | None = None) -> List[float]:
    return embed_transcript_segments([segment], model=model, api_key=api_key)[0]


def embed_transcript_texts(texts: Iterable[str], model: str = DEFAULT_EMBEDDING_MODEL, api_key: str | None = None) -> List[List[float]]:
    return embed_transcript_segments(list(texts), model=model, api_key=api_key)
