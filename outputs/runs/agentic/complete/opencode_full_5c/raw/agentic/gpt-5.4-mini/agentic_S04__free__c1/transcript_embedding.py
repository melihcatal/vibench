from speech_client import post
from speech_models import EmbeddingRequest


def transcript_embedding(segments: list) -> dict:
    req = EmbeddingRequest(segments=segments)
    return post(
        "/embeddings", {"model": "text-embedding-3-large", "input": req.segments}
    )
