from typing import Optional

import dashscope
from dashscope import TextEmbedding

from model_client import load_dashscope_api_key
from model_models import EmbeddingResult


EMBEDDING_MODEL = "text-embedding-v3"


def embed_platform_output(
    text: str,
    model: Optional[str] = None,
    dimensions: Optional[int] = None,
) -> EmbeddingResult:
    load_dashscope_api_key()

    model_id = model or EMBEDDING_MODEL

    params = {
        "model": model_id,
        "input": text,
    }

    if dimensions is not None:
        params["dimensions"] = dimensions

    response = TextEmbedding.call(**params)

    if response.status_code != 200:
        raise RuntimeError(
            f"DashScope Embedding API error: code={response.status_code}, message={response.message}"
        )

    embedding = []
    token_count = 0

    if response.output and "embeddings" in response.output:
        embeddings_list = response.output["embeddings"]
        if embeddings_list:
            embedding = embeddings_list[0].get("embedding", [])

    if response.usage:
        token_count = response.usage.get("total_tokens", 0)

    return EmbeddingResult(
        text=text,
        embedding=embedding,
        model=model_id,
        token_count=token_count,
        raw_response=response,
    )


def embed_platform_outputs_batch(
    texts: list,
    model: Optional[str] = None,
    dimensions: Optional[int] = None,
) -> list:
    load_dashscope_api_key()

    model_id = model or EMBEDDING_MODEL

    params = {
        "model": model_id,
        "input": texts,
    }

    if dimensions is not None:
        params["dimensions"] = dimensions

    response = TextEmbedding.call(**params)

    if response.status_code != 200:
        raise RuntimeError(
            f"DashScope Embedding API error: code={response.status_code}, message={response.message}"
        )

    results = []
    embeddings_list = response.output.get("embeddings", []) if response.output else []

    for idx, emb_item in enumerate(embeddings_list):
        token_count = 0
        if response.usage:
            token_count = response.usage.get("total_tokens", 0)

        results.append(
            EmbeddingResult(
                text=texts[idx] if idx < len(texts) else "",
                embedding=emb_item.get("embedding", []),
                model=model_id,
                token_count=token_count,
                raw_response=response,
            )
        )

    return results
