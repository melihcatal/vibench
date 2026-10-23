import os
from typing import Any, Dict, List, Optional

from openai import OpenAI


def _extract_segments(transcript: Any) -> List[Dict[str, Any]]:
    if transcript is None:
        return []
    if isinstance(transcript, dict):
        for key in ("segments", "items", "data", "results"):
            value = transcript.get(key)
            if isinstance(value, list):
                return [x for x in value if isinstance(x, dict)]
        if isinstance(transcript.get("transcript"), str):
            return [{"text": transcript["transcript"]}]
        if isinstance(transcript.get("text"), str):
            return [{"text": transcript["text"]}]
    if isinstance(transcript, list):
        return [x for x in transcript if isinstance(x, dict)]
    return []


def _segment_text(segment: Dict[str, Any]) -> str:
    for key in ("text", "transcript", "content", "segment"):
        value = segment.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return ""


def embed_transcript_segments(transcript: Any, model: Optional[str] = None) -> Dict[str, Any]:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is required")

    client = OpenAI(api_key=api_key)
    embedding_model = model or os.environ.get("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
    segments = _extract_segments(transcript)
    texts = [_segment_text(segment) for segment in segments]

    embeddings: List[Optional[List[float]]] = []
    if texts:
        response = client.embeddings.create(model=embedding_model, input=texts)
        by_index = {item.index: item.embedding for item in response.data}
        embeddings = [by_index.get(i) for i in range(len(texts))]

    enriched_segments: List[Dict[str, Any]] = []
    for index, segment in enumerate(segments):
        enriched = dict(segment)
        text = texts[index] if index < len(texts) else ""
        enriched["text"] = text
        enriched["embedding"] = embeddings[index] if index < len(embeddings) else None
        enriched_segments.append(enriched)

    return {"model": embedding_model, "segments": enriched_segments}
