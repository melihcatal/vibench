import os
from typing import Any, Dict, List, Optional

from openai import OpenAI


def _segment_text(segment: Any) -> str:
    if isinstance(segment, str):
        return segment
    if isinstance(segment, dict):
        for key in ("text", "transcript", "content", "segment_text"):
            value = segment.get(key)
            if isinstance(value, str) and value.strip():
                return value
    return str(segment)


def embed_transcript_segments(segments: List[Any], model: Optional[str] = None) -> Dict[str, Any]:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    embedding_model = model or os.environ.get("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
    texts = [_segment_text(segment) for segment in segments]
    response = client.embeddings.create(model=embedding_model, input=texts)
    embeddings = [item.embedding for item in response.data]
    return {"model": embedding_model, "segments": segments, "embeddings": embeddings}
