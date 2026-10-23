import os
from typing import Any, Dict, List, Optional, Sequence

from openai import OpenAI


def _client() -> OpenAI:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is required")
    return OpenAI(api_key=api_key)


def _segment_text(segment: Any) -> str:
    if isinstance(segment, str):
        return segment
    if isinstance(segment, dict):
        for key in ("text", "transcript", "content", "segment_text"):
            value = segment.get(key)
            if isinstance(value, str) and value.strip():
                return value
    return str(segment)


def embed_transcript_segments(segments: Sequence[Any], model: str = "text-embedding-3-small") -> List[Dict[str, Any]]:
    client = _client()
    texts = [_segment_text(segment) for segment in segments]
    response = client.embeddings.create(model=model, input=texts)
    embeddings_by_index: Dict[int, List[float]] = {item.index: item.embedding for item in response.data}
    results: List[Dict[str, Any]] = []
    for index, segment in enumerate(segments):
        results.append({"segment": segment, "embedding": embeddings_by_index.get(index)})
    return results


def embed_transcript_segment(segment: Any, model: str = "text-embedding-3-small") -> List[float]:
    return embed_transcript_segments([segment], model=model)[0]["embedding"]
