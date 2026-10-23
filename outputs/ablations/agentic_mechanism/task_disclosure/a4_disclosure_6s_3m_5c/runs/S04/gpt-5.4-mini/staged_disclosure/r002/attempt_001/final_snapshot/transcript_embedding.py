import os
from typing import Iterable, List, Sequence

from openai import OpenAI


OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")


def _segment_text(segment: object) -> str:
    if isinstance(segment, str):
        return segment
    if isinstance(segment, dict):
        for key in ("text", "content", "transcript", "segment"):
            value = segment.get(key)
            if isinstance(value, str) and value.strip():
                return value
        return " ".join(str(v) for v in segment.values() if isinstance(v, str) and v.strip())
    return str(segment)


def embed_transcript_segments(segments: Sequence[object], api_key: str | None = None) -> List[List[float]]:
    client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
    texts = [_segment_text(segment) for segment in segments]
    if not texts:
        return []
    response = client.embeddings.create(model=OPENAI_EMBEDDING_MODEL, input=texts)
    return [item.embedding for item in response.data]


def embed_transcript_segment(segment: object, api_key: str | None = None) -> List[float]:
    return embed_transcript_segments([segment], api_key=api_key)[0]
