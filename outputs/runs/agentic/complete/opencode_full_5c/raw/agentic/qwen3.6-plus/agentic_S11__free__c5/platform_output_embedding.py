from typing import Optional, List
from openai import OpenAI
from openai.types import CreateEmbeddingResponse
from model_client import create_openai_client
from model_models import EmbeddingResult


DEFAULT_EMBEDDING_MODEL = "text-embedding-3-small"
DEFAULT_EMBEDDING_DIMENSIONS = 1536


def embed_platform_output(
    text: str,
    model: Optional[str] = None,
    dimensions: Optional[int] = None,
    client: Optional[OpenAI] = None,
) -> EmbeddingResult:
    if client is None:
        client = create_openai_client()
    target_model = model or DEFAULT_EMBEDDING_MODEL
    kwargs: dict = {
        "model": target_model,
        "input": text,
    }
    if dimensions is not None:
        kwargs["dimensions"] = dimensions
    response: CreateEmbeddingResponse = client.embeddings.create(**kwargs)
    embedding_data = response.data[0]
    embedding = embedding_data.embedding
    usage = response.usage
    actual_dimensions = len(embedding)
    return EmbeddingResult(
        embedding=embedding,
        model=response.model,
        input_text=text,
        embedding_dimensions=actual_dimensions,
        prompt_tokens=usage.prompt_tokens if usage else 0,
        request_id=getattr(response, "id", None),
        raw_response=response,
    )


def embed_multiple_outputs(
    texts: List[str],
    model: Optional[str] = None,
    dimensions: Optional[int] = None,
    client: Optional[OpenAI] = None,
) -> List[EmbeddingResult]:
    if client is None:
        client = create_openai_client()
    target_model = model or DEFAULT_EMBEDDING_MODEL
    kwargs: dict = {
        "model": target_model,
        "input": texts,
    }
    if dimensions is not None:
        kwargs["dimensions"] = dimensions
    response: CreateEmbeddingResponse = client.embeddings.create(**kwargs)
    results = []
    usage = response.usage
    for i, embedding_data in enumerate(response.data):
        embedding = embedding_data.embedding
        results.append(
            EmbeddingResult(
                embedding=embedding,
                model=response.model,
                input_text=texts[i],
                embedding_dimensions=len(embedding),
                prompt_tokens=usage.prompt_tokens if usage else 0,
                request_id=getattr(response, "id", None),
                raw_response=response,
            )
        )
    return results


def compute_similarity(
    embedding_a: List[float],
    embedding_b: List[float],
) -> float:
    if len(embedding_a) != len(embedding_b):
        raise ValueError("Embeddings must have the same dimensions")
    dot_product = sum(a * b for a, b in zip(embedding_a, embedding_b))
    magnitude_a = sum(a * a for a in embedding_a) ** 0.5
    magnitude_b = sum(b * b for b in embedding_b) ** 0.5
    if magnitude_a == 0 or magnitude_b == 0:
        return 0.0
    return dot_product / (magnitude_a * magnitude_b)


def embed_and_compare(
    text_a: str,
    text_b: str,
    model: Optional[str] = None,
    dimensions: Optional[int] = None,
    client: Optional[OpenAI] = None,
) -> dict:
    if client is None:
        client = create_openai_client()
    result_a = embed_platform_output(
        text_a, model=model, dimensions=dimensions, client=client
    )
    result_b = embed_platform_output(
        text_b, model=model, dimensions=dimensions, client=client
    )
    similarity = compute_similarity(result_a.embedding, result_b.embedding)
    return {
        "embedding_a": result_a,
        "embedding_b": result_b,
        "similarity": similarity,
        "model": result_a.model,
        "provider": "openai",
        "api_endpoint": "https://api.openai.com/v1/embeddings",
    }
