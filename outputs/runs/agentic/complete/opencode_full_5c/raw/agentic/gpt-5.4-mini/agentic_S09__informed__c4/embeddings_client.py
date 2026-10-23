import os
from typing import List

from openai import OpenAI

from embeddings_models import (
    EmbeddingRequest,
    EmbeddingResponse,
    normalize_embedding,
    normalize_texts,
)


DEFAULT_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")


def get_client() -> OpenAI:
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def embed_texts(texts) -> EmbeddingResponse:
    client = get_client()
    normalized = normalize_texts(texts)
    request = EmbeddingRequest(input=normalized, model=DEFAULT_EMBEDDING_MODEL)
    response = client.embeddings.create(model=request.model, input=request.input)
    embeddings = [normalize_embedding(item.embedding) for item in response.data]
    return EmbeddingResponse(embeddings=embeddings, model=request.model)


def cosine_similarity(left: List[float], right: List[float]) -> float:
    dot = sum(a * b for a, b in zip(left, right))
    left_norm = sum(a * a for a in left) ** 0.5
    right_norm = sum(b * b for b in right) ** 0.5
    return dot / (left_norm * right_norm) if left_norm and right_norm else 0.0
