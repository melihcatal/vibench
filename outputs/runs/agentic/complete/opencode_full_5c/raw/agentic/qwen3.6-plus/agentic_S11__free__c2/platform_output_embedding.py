from model_client import create_openai_client, OPENAI_API_BASE
from model_models import EmbeddingResult, PlatformUsageInfo


def generate_platform_output_embedding(
    text: str,
    model: str = "text-embedding-3-small",
    dimensions: int | None = None,
) -> EmbeddingResult:
    client = create_openai_client(base_url=OPENAI_API_BASE)
    params = {"input": text, "model": model}
    if dimensions is not None:
        params["dimensions"] = dimensions
    response = client.embeddings.create(**params)
    embedding_data = response.data[0]
    usage = None
    if response.usage:
        usage = PlatformUsageInfo.from_openai_usage(response.usage)
    return EmbeddingResult(
        embedding=embedding_data.embedding,
        model=response.model,
        usage=usage,
        raw_result=response,
    )


def generate_platform_output_embeddings(
    texts: list[str],
    model: str = "text-embedding-3-small",
    dimensions: int | None = None,
) -> list[EmbeddingResult]:
    client = create_openai_client(base_url=OPENAI_API_BASE)
    params = {"input": texts, "model": model}
    if dimensions is not None:
        params["dimensions"] = dimensions
    response = client.embeddings.create(**params)
    results = []
    for item in response.data:
        results.append(
            EmbeddingResult(
                embedding=item.embedding,
                model=response.model,
                raw_result=response,
            )
        )
    return results
