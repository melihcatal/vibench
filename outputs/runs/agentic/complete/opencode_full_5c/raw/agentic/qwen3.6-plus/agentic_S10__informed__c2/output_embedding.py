import os
from typing import Optional

from openai import OpenAI

from model_models import EmbeddingResult


def _get_openai_client() -> OpenAI:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is not set")
    return OpenAI(api_key=api_key)


def generate_embedding(
    text: str,
    model: str = "text-embedding-3-small",
    dimensions: Optional[int] = None,
) -> EmbeddingResult:
    client = _get_openai_client()
    kwargs: dict = {"input": text, "model": model}
    if dimensions:
        kwargs["dimensions"] = dimensions

    response = client.embeddings.create(**kwargs)
    data = response.data[0]
    return EmbeddingResult(
        embedding=data.embedding,
        model=response.model,
        usage={
            "prompt_tokens": response.usage.prompt_tokens,
            "total_tokens": response.usage.total_tokens,
        },
        raw_response=response,
    )


def generate_embeddings_batch(
    texts: list[str],
    model: str = "text-embedding-3-small",
    dimensions: Optional[int] = None,
) -> list[EmbeddingResult]:
    client = _get_openai_client()
    kwargs: dict = {"input": texts, "model": model}
    if dimensions:
        kwargs["dimensions"] = dimensions

    response = client.embeddings.create(**kwargs)
    results = []
    for item in response.data:
        results.append(
            EmbeddingResult(
                embedding=item.embedding,
                model=response.model,
                usage={
                    "prompt_tokens": response.usage.prompt_tokens,
                    "total_tokens": response.usage.total_tokens,
                },
                raw_response=response,
            )
        )
    return results


def cosine_similarity(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = sum(x * x for x in a) ** 0.5
    norm_b = sum(x * x for x in b) ** 0.5
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


def find_most_similar(
    query_text: str,
    candidate_texts: list[str],
    model: str = "text-embedding-3-small",
    top_k: int = 5,
) -> list[tuple[int, float]]:
    query_result = generate_embedding(query_text, model=model)
    query_vec = query_result.embedding

    candidate_results = generate_embeddings_batch(candidate_texts, model=model)
    similarities = []
    for i, cand in enumerate(candidate_results):
        sim = cosine_similarity(query_vec, cand.embedding)
        similarities.append((i, sim))

    similarities.sort(key=lambda x: x[1], reverse=True)
    return similarities[:top_k]
