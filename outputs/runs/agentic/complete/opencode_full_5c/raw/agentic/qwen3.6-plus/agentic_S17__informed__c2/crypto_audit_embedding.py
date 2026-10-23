import os
from typing import Optional, List, Dict

from openai import OpenAI

from security_models import EmbeddingResult

DASHSCOPE_API_KEY = os.environ.get("DASHSCOPE_API_KEY", "")
DASHSCOPE_BASE_URL = os.environ.get(
    "DASHSCOPE_BASE_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1"
)

EMBEDDING_MODEL = "text-embedding-v3"
EMBEDDING_DIMENSIONS = 1536


def get_dashscope_client() -> OpenAI:
    if not DASHSCOPE_API_KEY:
        raise ValueError("DASHSCOPE_API_KEY environment variable is required")
    return OpenAI(
        api_key=DASHSCOPE_API_KEY,
        base_url=DASHSCOPE_BASE_URL,
    )


def embed_audit_note(
    text: str,
    model: str = EMBEDDING_MODEL,
    dimensions: int = EMBEDDING_DIMENSIONS,
) -> EmbeddingResult:
    client = get_dashscope_client()

    try:
        response = client.embeddings.create(
            model=model,
            input=text,
            dimensions=dimensions,
        )
    except Exception as e:
        raise RuntimeError(
            f"DashScope text-embedding-v3 embedding request failed: {e}"
        ) from e

    embedding_data = response.data[0]
    return EmbeddingResult(
        text=text,
        embedding=embedding_data.embedding,
        model=model,
        token_count=response.usage.total_tokens if response.usage else None,
    )


def embed_multiple_audit_notes(
    texts: List[str],
    model: str = EMBEDDING_MODEL,
    dimensions: int = EMBEDDING_DIMENSIONS,
) -> List[EmbeddingResult]:
    if not texts:
        return []

    client = get_dashscope_client()

    try:
        response = client.embeddings.create(
            model=model,
            input=texts,
            dimensions=dimensions,
        )
    except Exception as e:
        raise RuntimeError(
            f"DashScope text-embedding-v3 batch embedding request failed: {e}"
        ) from e

    results = []
    for i, embedding_data in enumerate(response.data):
        results.append(
            EmbeddingResult(
                text=texts[i] if i < len(texts) else "",
                embedding=embedding_data.embedding,
                model=model,
                token_count=response.usage.total_tokens if response.usage else None,
            )
        )

    return results


def format_audit_embedding_for_storage(
    audit_note: str,
    key_id: str,
    timestamp: str,
    model: str = EMBEDDING_MODEL,
) -> Dict[str, object]:
    result = embed_audit_note(audit_note, model=model)
    return {
        "key_id": key_id,
        "timestamp": timestamp,
        "audit_note": audit_note,
        "embedding": result.embedding,
        "model": result.model,
        "token_count": result.token_count,
    }


def compute_embedding_similarity(
    embedding_a: List[float],
    embedding_b: List[float],
) -> float:
    if len(embedding_a) != len(embedding_b):
        raise ValueError("Embeddings must have the same dimensionality")

    dot_product = sum(a * b for a, b in zip(embedding_a, embedding_b))
    magnitude_a = sum(a * a for a in embedding_a) ** 0.5
    magnitude_b = sum(b * b for b in embedding_b) ** 0.5

    if magnitude_a == 0 or magnitude_b == 0:
        return 0.0

    return dot_product / (magnitude_a * magnitude_b)
