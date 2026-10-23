import os
from typing import Any, Dict, List, Optional

from openai import OpenAI


def _extract_segments(transcript_result: Dict[str, Any]) -> List[Dict[str, Any]]:
    segments = transcript_result.get("segments")
    if isinstance(segments, list):
        return [segment for segment in segments if isinstance(segment, dict)]
    return []


def _segment_text(segment: Dict[str, Any]) -> str:
    for key in ("text", "transcript", "content"):
        value = segment.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return ""


def _segment_id(segment: Dict[str, Any], index: int) -> str:
    for key in ("id", "segment_id", "index"):
        value = segment.get(key)
        if value is not None:
            return str(value)
    return str(index)


def embed_transcript_segments(
    transcript_result: Dict[str, Any],
    *,
    model: str = "text-embedding-3-small",
    api_key: Optional[str] = None,
) -> List[Dict[str, Any]]:
    client = OpenAI(api_key=api_key or os.environ.get("OPENAI_API_KEY"))
    segments = _extract_segments(transcript_result)
    texts = [_segment_text(segment) for segment in segments]
    non_empty = [(idx, text) for idx, text in enumerate(texts) if text]
    if not non_empty:
        return []
    embeddings = client.embeddings.create(model=model, input=[text for _, text in non_empty])
    output: List[Dict[str, Any]] = []
    for (original_index, text), item in zip(non_empty, embeddings.data):
        segment = segments[original_index]
        output.append(
            {
                "segment_id": _segment_id(segment, original_index),
                "text": text,
                "embedding": item.embedding,
                "start": segment.get("start"),
                "end": segment.get("end"),
                "speaker": segment.get("speaker"),
            }
        )
    return output
