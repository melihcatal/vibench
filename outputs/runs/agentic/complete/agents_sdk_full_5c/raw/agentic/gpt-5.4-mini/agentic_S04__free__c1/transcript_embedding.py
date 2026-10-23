from __future__ import annotations

from openai import OpenAI

from speech_client import OPENAI_EMBEDDING_MODEL, get_client, normalize_text
from speech_models import EmbeddingRequest


def transcript_embedding(transcript_segments: list[str]) -> dict:
    client: OpenAI = get_client()
    request = EmbeddingRequest(transcript_segments=[normalize_text(segment) for segment in transcript_segments])
    response = client.embeddings.create(
        model=request.model or OPENAI_EMBEDDING_MODEL,
        input=request.transcript_segments,
    )
    vectors = [item.embedding for item in response.data]
    return {"model": response.model, "embeddings": vectors, "raw": response.model_dump()}
