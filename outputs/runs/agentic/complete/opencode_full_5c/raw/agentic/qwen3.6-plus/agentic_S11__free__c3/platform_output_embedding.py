from __future__ import annotations

from typing import Dict, List, Optional

from model_client import get_platform_client, DEFAULT_EMBEDDING_MODEL
from model_models import EmbeddingResult


def generate_platform_output_embedding(
    text: str,
    model: str = DEFAULT_EMBEDDING_MODEL,
    dimensions: Optional[int] = None,
    api_key: Optional[str] = None,
    organization: Optional[str] = None,
    project: Optional[str] = None,
) -> EmbeddingResult:
    client = get_platform_client(
        api_key=api_key,
        organization=organization,
        project=project,
    )

    result = client.create_embedding(text=text, model=model, dimensions=dimensions)

    return EmbeddingResult(
        embedding=result["embedding"],
        model_id=result["model"],
        usage_prompt_tokens=result["usage"]["prompt_tokens"],
        raw_response=result["raw_response"],
    )


def generate_batch_embeddings(
    texts: List[str],
    model: str = DEFAULT_EMBEDDING_MODEL,
    dimensions: Optional[int] = None,
    api_key: Optional[str] = None,
    organization: Optional[str] = None,
    project: Optional[str] = None,
) -> List[EmbeddingResult]:
    results = []
    for text in texts:
        result = generate_platform_output_embedding(
            text=text,
            model=model,
            dimensions=dimensions,
            api_key=api_key,
            organization=organization,
            project=project,
        )
        results.append(result)
    return results


def compute_cosine_similarity(
    embedding_a: List[float],
    embedding_b: List[float],
) -> float:
    if len(embedding_a) != len(embedding_b):
        raise ValueError("Embeddings must have the same dimension")

    dot_product = sum(a * b for a, b in zip(embedding_a, embedding_b))
    magnitude_a = sum(a * a for a in embedding_a) ** 0.5
    magnitude_b = sum(b * b for b in embedding_b) ** 0.5

    if magnitude_a == 0 or magnitude_b == 0:
        return 0.0

    return dot_product / (magnitude_a * magnitude_b)


def embed_and_compare(
    text_a: str,
    text_b: str,
    model: str = DEFAULT_EMBEDDING_MODEL,
    api_key: Optional[str] = None,
    organization: Optional[str] = None,
    project: Optional[str] = None,
) -> Dict:
    result_a = generate_platform_output_embedding(
        text=text_a,
        model=model,
        api_key=api_key,
        organization=organization,
        project=project,
    )
    result_b = generate_platform_output_embedding(
        text=text_b,
        model=model,
        api_key=api_key,
        organization=organization,
        project=project,
    )

    similarity = compute_cosine_similarity(result_a.embedding, result_b.embedding)

    return {
        "embedding_a": result_a,
        "embedding_b": result_b,
        "similarity": similarity,
    }


def generate_embedding_for_retrieval(
    text: str,
    model: str = DEFAULT_EMBEDDING_MODEL,
    dimensions: int = 1536,
    api_key: Optional[str] = None,
    organization: Optional[str] = None,
    project: Optional[str] = None,
) -> EmbeddingResult:
    return generate_platform_output_embedding(
        text=text,
        model=model,
        dimensions=dimensions,
        api_key=api_key,
        organization=organization,
        project=project,
    )
