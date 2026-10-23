from typing import Any, Dict, List

from openai import OpenAI

from speech_client import get_openai_client, load_speech_settings
from speech_models import TranscriptEmbeddingRequest


def transcript_embedding(segments: List[str]) -> Dict[str, Any]:
    settings = load_speech_settings()
    client = get_openai_client(settings)
    request = TranscriptEmbeddingRequest(segments=segments)
    embeddings = client.embeddings.create(
        model=settings.embedding_model,
        input=request.segments,
    )
    data = embeddings.model_dump() if hasattr(embeddings, "model_dump") else embeddings.dict()
    return {"model": settings.embedding_model, "embeddings": data}
