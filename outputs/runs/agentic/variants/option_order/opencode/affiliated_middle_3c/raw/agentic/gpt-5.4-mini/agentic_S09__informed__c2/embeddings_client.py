import os
from typing import List, Sequence

from openai import OpenAI

from embeddings_models import EmbeddingRequest, EmbeddingResponse, normalize_embeddings


def get_openai_client() -> OpenAI:
    return OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def get_embedding_model() -> str:
    return os.environ.get("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")


def embed_texts(texts: Sequence[str], model: str | None = None) -> EmbeddingResponse:
    client = get_openai_client()
    request = EmbeddingRequest(inputs=texts, model=model or get_embedding_model())
    response = client.embeddings.create(model=request.model, input=list(request.inputs))
    payload = (
        response.model_dump() if hasattr(response, "model_dump") else response.to_dict()
    )
    return EmbeddingResponse(
        embeddings=normalize_embeddings(payload), model=request.model, raw=payload
    )


def cosine_similarity(a: List[float], b: List[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = sum(x * x for x in a) ** 0.5
    norm_b = sum(y * y for y in b) ** 0.5
    return dot / (norm_a * norm_b) if norm_a and norm_b else 0.0
