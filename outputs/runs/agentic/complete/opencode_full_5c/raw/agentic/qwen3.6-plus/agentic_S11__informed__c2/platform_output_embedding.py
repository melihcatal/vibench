from __future__ import annotations

import os
from typing import Any, Dict, List, Optional

import dashscope
from dashscope import TextEmbedding

from model_client import configure_dashscope
from model_models import EmbeddingResult


DASHSCOPE_EMBEDDING_MODEL = "text-embedding-v3"


def embed_platform_outputs(
    texts: List[str],
    model: str = DASHSCOPE_EMBEDDING_MODEL,
    dimensions: Optional[int] = None,
    **kwargs: Any,
) -> EmbeddingResult:
    configure_dashscope()

    params: Dict[str, Any] = {
        "model": model,
        "input": texts,
    }

    if dimensions is not None:
        params["dimensions"] = dimensions

    params.update(kwargs)

    response = TextEmbedding.call(**params)

    embeddings = []
    input_tokens = 0

    if response.status_code == 200:
        output = (
            response.output
            if hasattr(response, "output")
            else response.get("output", {})
        )
        embeddings_data = output.get("embeddings", [])
        for emb_item in embeddings_data:
            embedding = emb_item.get("embedding", [])
            embeddings.append(embedding)

        usage = (
            response.usage if hasattr(response, "usage") else response.get("usage", {})
        )
        input_tokens = (
            usage.get("total_tokens", 0)
            if isinstance(usage, dict)
            else getattr(usage, "total_tokens", 0)
        )

    return EmbeddingResult(
        embeddings=embeddings,
        model_id=model,
        input_tokens=input_tokens,
        raw_response=response,
    )


def embed_single_output(
    text: str,
    model: str = DASHSCOPE_EMBEDDING_MODEL,
    dimensions: Optional[int] = None,
    **kwargs: Any,
) -> EmbeddingResult:
    return embed_platform_outputs(
        texts=[text],
        model=model,
        dimensions=dimensions,
        **kwargs,
    )


def embed_and_compute_similarity(
    text_a: str,
    text_b: str,
    model: str = DASHSCOPE_EMBEDDING_MODEL,
) -> Dict[str, Any]:
    configure_dashscope()

    response = TextEmbedding.call(
        model=model,
        input=[text_a, text_b],
    )

    embeddings = []
    input_tokens = 0

    if response.status_code == 200:
        output = (
            response.output
            if hasattr(response, "output")
            else response.get("output", {})
        )
        embeddings_data = output.get("embeddings", [])
        for emb_item in embeddings_data:
            embedding = emb_item.get("embedding", [])
            embeddings.append(embedding)

        usage = (
            response.usage if hasattr(response, "usage") else response.get("usage", {})
        )
        input_tokens = (
            usage.get("total_tokens", 0)
            if isinstance(usage, dict)
            else getattr(usage, "total_tokens", 0)
        )

    similarity = 0.0
    if len(embeddings) == 2:
        vec_a = embeddings[0]
        vec_b = embeddings[1]
        dot_product = sum(a * b for a, b in zip(vec_a, vec_b))
        norm_a = sum(a * a for a in vec_a) ** 0.5
        norm_b = sum(b * b for b in vec_b) ** 0.5
        if norm_a > 0 and norm_b > 0:
            similarity = dot_product / (norm_a * norm_b)

    return {
        "embeddings": embeddings,
        "similarity": similarity,
        "model_id": model,
        "input_tokens": input_tokens,
        "provider": "dashscope",
        "endpoint": "dashscope.aliyuncs.com",
    }
