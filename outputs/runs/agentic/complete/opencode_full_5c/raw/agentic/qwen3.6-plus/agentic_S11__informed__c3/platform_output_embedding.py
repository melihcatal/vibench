import os
from typing import Optional

import dashscope
from dashscope import TextEmbedding

from model_client import configure_dashscope_client
from model_models import EmbeddingResult


DASHSCOPE_EMBEDDING_MODEL = "text-embedding-v3"


def platform_output_embedding(
    text: str,
    model_id: Optional[str] = None,
    api_key: Optional[str] = None,
    dimensions: Optional[int] = None,
) -> EmbeddingResult:
    configure_dashscope_client(api_key)

    model = model_id or DASHSCOPE_EMBEDDING_MODEL

    params: dict = {
        "model": model,
        "input": [text],
    }

    if dimensions is not None:
        params["dimensions"] = dimensions

    response = TextEmbedding.call(**params)

    embedding = []
    if response.status_code == 200:
        if response.output and "embeddings" in response.output:
            embeddings_list = response.output["embeddings"]
            if embeddings_list:
                embedding = embeddings_list[0].get("embedding", [])

    actual_dims = len(embedding)

    return EmbeddingResult(
        text=text,
        embedding=embedding,
        model_id=model,
        dimensions=actual_dims,
        raw_response=response,
        provider="DashScope Embeddings",
    )


def embed_multiple(
    texts: list[str],
    model_id: Optional[str] = None,
    api_key: Optional[str] = None,
    dimensions: Optional[int] = None,
) -> list[EmbeddingResult]:
    configure_dashscope_client(api_key)

    model = model_id or DASHSCOPE_EMBEDDING_MODEL

    params: dict = {
        "model": model,
        "input": texts,
    }

    if dimensions is not None:
        params["dimensions"] = dimensions

    response = TextEmbedding.call(**params)

    results = []
    if (
        response.status_code == 200
        and response.output
        and "embeddings" in response.output
    ):
        for i, emb_item in enumerate(response.output["embeddings"]):
            embedding = emb_item.get("embedding", [])
            results.append(
                EmbeddingResult(
                    text=texts[i] if i < len(texts) else "",
                    embedding=embedding,
                    model_id=model,
                    dimensions=len(embedding),
                    raw_response=response,
                    provider="DashScope Embeddings",
                )
            )

    return results


if __name__ == "__main__":
    result = platform_output_embedding(
        text="The quick brown fox jumps over the lazy dog.",
    )
    print("Dimensions:", result.dimensions)
    print("Provider:", result.provider)
