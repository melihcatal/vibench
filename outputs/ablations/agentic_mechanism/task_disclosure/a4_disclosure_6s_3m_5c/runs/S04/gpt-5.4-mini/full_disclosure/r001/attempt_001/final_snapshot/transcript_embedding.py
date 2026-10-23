import os
from typing import Any, Dict, Iterable, List, Mapping, Optional, Sequence, Union

from openai import OpenAI


def _extract_text(segment: Any) -> str:
    if isinstance(segment, str):
        return segment
    if isinstance(segment, Mapping):
        for key in ("text", "content", "transcript", "segment", "utterance"):
            value = segment.get(key)
            if isinstance(value, str):
                return value
    return str(segment)


def _normalize_segments(segments: Union[str, Sequence[Any]]) -> List[str]:
    if isinstance(segments, str):
        return [segments]
    return [text for text in (_extract_text(segment).strip() for segment in segments) if text]


def embed_transcript_segments(
    segments: Union[str, Sequence[Any]],
    model: str = "text-embedding-3-small",
    api_key: Optional[str] = None,
) -> Dict[str, Any]:
    client = OpenAI(api_key=api_key or os.environ.get("OPENAI_API_KEY"))
    texts = _normalize_segments(segments)
    response = client.embeddings.create(model=model, input=texts)
    embeddings = [item.embedding for item in response.data]
    return {"model": model, "texts": texts, "embeddings": embeddings}


def embed_transcript_segment(
    segment: Any,
    model: str = "text-embedding-3-small",
    api_key: Optional[str] = None,
) -> List[float]:
    result = embed_transcript_segments([segment], model=model, api_key=api_key)
    return result["embeddings"][0]
