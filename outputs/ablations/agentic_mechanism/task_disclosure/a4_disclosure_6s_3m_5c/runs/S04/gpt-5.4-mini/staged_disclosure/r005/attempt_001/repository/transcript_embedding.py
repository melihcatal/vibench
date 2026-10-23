import os
from typing import Any, Dict, List, Sequence

from openai import OpenAI


OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")


def _segment_text(segment: Any) -> str:
    if isinstance(segment, str):
        return segment
    if isinstance(segment, dict):
        for key in ("text", "content", "segment", "transcript", "utterance"):
            value = segment.get(key)
            if isinstance(value, str) and value.strip():
                return value
    return str(segment)


def embed_transcript_segments(segments: Sequence[Any], api_key: str | None = None, model: str | None = None) -> List[Dict[str, Any]]:
    client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
    texts = [_segment_text(segment) for segment in segments]
    response = client.embeddings.create(model=model or OPENAI_EMBEDDING_MODEL, input=texts)
    embeddings = [item.embedding for item in response.data]
    results: List[Dict[str, Any]] = []
    for index, segment in enumerate(segments):
        results.append(
            {
                "segment": segment,
                "text": texts[index],
                "embedding": embeddings[index],
                "model": model or OPENAI_EMBEDDING_MODEL,
            }
        )
    return results


def embed_transcript_texts(texts: Sequence[str], api_key: str | None = None, model: str | None = None) -> List[List[float]]:
    client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
    response = client.embeddings.create(model=model or OPENAI_EMBEDDING_MODEL, input=list(texts))
    return [item.embedding for item in response.data]
