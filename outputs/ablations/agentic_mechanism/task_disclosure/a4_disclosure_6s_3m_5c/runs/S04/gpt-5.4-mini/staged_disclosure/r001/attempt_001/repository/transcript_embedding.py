import os
from typing import Iterable, List, Sequence

import openai


DEFAULT_EMBEDDING_MODEL = "text-embedding-3-small"


def _get_client() -> openai.OpenAI:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is required")
    return openai.OpenAI(api_key=api_key)


def _segment_text(segment: object) -> str:
    if isinstance(segment, str):
        return segment
    if isinstance(segment, dict):
        for key in ("text", "content", "segment", "transcript"):
            value = segment.get(key)
            if isinstance(value, str) and value.strip():
                return value
        return " ".join(str(v) for v in segment.values() if v is not None)
    return str(segment)


def embed_transcript_segments(
    segments: Sequence[object],
    model: str = DEFAULT_EMBEDDING_MODEL,
) -> List[List[float]]:
    client = _get_client()
    texts = [_segment_text(segment) for segment in segments]
    if not texts:
        return []
    response = client.embeddings.create(model=model, input=texts)
    return [item.embedding for item in response.data]


def embed_transcript_segment(segment: object, model: str = DEFAULT_EMBEDDING_MODEL) -> List[float]:
    return embed_transcript_segments([segment], model=model)[0]


def embed_transcript_segments_iter(
    segments: Iterable[object],
    model: str = DEFAULT_EMBEDDING_MODEL,
) -> List[List[float]]:
    return embed_transcript_segments(list(segments), model=model)
