from __future__ import annotations

from typing import Any, Dict, List

from openai import OpenAI

from speech_client import require_openai_api_key
from speech_models import EmbeddingResult


def transcript_embedding(segments: List[Dict[str, Any]]) -> Dict[str, Any]:
    client = OpenAI(api_key=require_openai_api_key())
    inputs = [segment.get("text", "") for segment in segments]
    response = client.embeddings.create(model="text-embedding-3-large", input=inputs)
    vectors = [item.embedding for item in response.data]
    result = EmbeddingResult(
        vectors=vectors, provider="openai", model="text-embedding-3-large"
    )
    return {
        "provider": result.provider,
        "model": result.model,
        "vectors": result.vectors,
    }
