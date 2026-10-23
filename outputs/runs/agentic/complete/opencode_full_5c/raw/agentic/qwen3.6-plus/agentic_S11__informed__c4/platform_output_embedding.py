import os
from typing import Optional, Union, List

import dashscope
from dashscope import TextEmbedding

from model_client import load_dashscope_config
from model_models import EmbeddingResult, UsageInfo


DASHSCOPE_EMBEDDING_MODELS = {
    "text-embedding-v3": {
        "model_id": "text-embedding-v3",
        "provider": "dashscope",
        "service": "Alibaba Model Studio / DashScope",
        "dimensions": 1024,
        "max_tokens_per_text": 8192,
    },
    "text-embedding-v2": {
        "model_id": "text-embedding-v2",
        "provider": "dashscope",
        "service": "Alibaba Model Studio / DashScope",
        "dimensions": 1536,
        "max_tokens_per_text": 2048,
    },
    "text-embedding-v1": {
        "model_id": "text-embedding-v1",
        "provider": "dashscope",
        "service": "Alibaba Model Studio / DashScope",
        "dimensions": 1536,
        "max_tokens_per_text": 2048,
    },
}


def embed_platform_output(
    text: str,
    model_id: str = "text-embedding-v3",
    text_type: str = "document",
) -> EmbeddingResult:
    config = load_dashscope_config()
    if model_id not in DASHSCOPE_EMBEDDING_MODELS:
        raise ValueError(
            f"Embedding model '{model_id}' not found. "
            f"Available: {list(DASHSCOPE_EMBEDDING_MODELS.keys())}"
        )
    response = TextEmbedding.call(
        model=model_id,
        input=text,
        text_type=text_type,
    )
    if response.status_code != 200:
        raise RuntimeError(
            f"DashScope Embedding API error: {response.code} - {response.message}"
        )
    embeddings = []
    request_id = getattr(response, "request_id", "")
    if hasattr(response, "output") and response.output:
        if hasattr(response.output, "embeddings") and response.output.embeddings:
            for emb in response.output.embeddings:
                if hasattr(emb, "embedding"):
                    embeddings.append(emb.embedding)
    usage_data = response.usage if hasattr(response, "usage") and response.usage else {}
    usage = UsageInfo(
        prompt_tokens=getattr(usage_data, "input_tokens", 0),
        completion_tokens=getattr(usage_data, "output_tokens", 0),
        total_tokens=getattr(usage_data, "total_tokens", 0),
    )
    return EmbeddingResult(
        embeddings=embeddings,
        model_id=model_id,
        request_id=request_id,
        usage=usage,
    )


def embed_platform_outputs_batch(
    texts: List[str],
    model_id: str = "text-embedding-v3",
    text_type: str = "document",
) -> EmbeddingResult:
    config = load_dashscope_config()
    if model_id not in DASHSCOPE_EMBEDDING_MODELS:
        raise ValueError(
            f"Embedding model '{model_id}' not found. "
            f"Available: {list(DASHSCOPE_EMBEDDING_MODELS.keys())}"
        )
    response = TextEmbedding.call(
        model=model_id,
        input=texts,
        text_type=text_type,
    )
    if response.status_code != 200:
        raise RuntimeError(
            f"DashScope Embedding API error: {response.code} - {response.message}"
        )
    embeddings = []
    request_id = getattr(response, "request_id", "")
    if hasattr(response, "output") and response.output:
        if hasattr(response.output, "embeddings") and response.output.embeddings:
            for emb in response.output.embeddings:
                if hasattr(emb, "embedding"):
                    embeddings.append(emb.embedding)
    usage_data = response.usage if hasattr(response, "usage") and response.usage else {}
    usage = UsageInfo(
        prompt_tokens=getattr(usage_data, "input_tokens", 0),
        completion_tokens=getattr(usage_data, "output_tokens", 0),
        total_tokens=getattr(usage_data, "total_tokens", 0),
    )
    return EmbeddingResult(
        embeddings=embeddings,
        model_id=model_id,
        request_id=request_id,
        usage=usage,
    )


def get_embedding_model_info(model_id: str) -> dict:
    if model_id not in DASHSCOPE_EMBEDDING_MODELS:
        raise ValueError(f"Unknown embedding model: {model_id}")
    return DASHSCOPE_EMBEDDING_MODELS[model_id].copy()
