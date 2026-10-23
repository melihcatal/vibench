from __future__ import annotations

from typing import Optional

from openai import OpenAI

from model_client import PlatformClientConfig, create_openai_client
from model_models import EmbeddingResult, PlatformUsage


def embed_platform_output(
    text: str,
    model: str = "text-embedding-3-small",
    dimensions: Optional[int] = None,
    client: Optional[OpenAI] = None,
    config: Optional[PlatformClientConfig] = None,
) -> EmbeddingResult:
    openai_client = client or create_openai_client(config)

    kwargs: dict = {
        "model": model,
        "input": text,
    }
    if dimensions is not None:
        kwargs["dimensions"] = dimensions

    response = openai_client.embeddings.create(**kwargs)

    data = response.data[0]
    embedding = data.embedding

    usage_info = response.usage
    usage = PlatformUsage(
        prompt_tokens=usage_info.prompt_tokens,
        completion_tokens=0,
        total_tokens=usage_info.total_tokens,
        raw=usage_info.model_dump() if hasattr(usage_info, "model_dump") else None,
    )

    return EmbeddingResult(
        embedding=embedding,
        model=response.model,
        usage=usage,
        raw=response,
    )


def embed_multiple_platform_outputs(
    texts: list[str],
    model: str = "text-embedding-3-small",
    dimensions: Optional[int] = None,
    client: Optional[OpenAI] = None,
    config: Optional[PlatformClientConfig] = None,
) -> list[EmbeddingResult]:
    if not texts:
        return []

    openai_client = client or create_openai_client(config)

    kwargs: dict = {
        "model": model,
        "input": texts,
    }
    if dimensions is not None:
        kwargs["dimensions"] = dimensions

    response = openai_client.embeddings.create(**kwargs)

    results = []
    for item in response.data:
        results.append(
            EmbeddingResult(
                embedding=item.embedding,
                model=response.model,
                raw=response,
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


if __name__ == "__main__":
    result = embed_platform_output("Hello, world!")
    print(f"Embedding dimensions: {len(result.embedding)}")
    print(f"Model: {result.model}")
