from __future__ import annotations

from typing import Any, Dict, Iterable, List

from speech_client import load_config
from openai import OpenAI


def transcript_embedding(segments: Iterable[Dict[str, Any]], model: str = "text-embedding-3-large") -> Dict[str, Any]:
    config = load_config()
    client = OpenAI(api_key=config.api_key)
    texts = [str(segment.get("text", "")) for segment in segments]
    response = client.embeddings.create(model=model, input=texts)
    embeddings = [item.embedding for item in response.data]
    return {"model": model, "embeddings": embeddings}
