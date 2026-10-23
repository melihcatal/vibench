"""
[LATER-STEP] Embed platform outputs for evaluation or retrieval using
Amazon Titan Embeddings via Bedrock Runtime.

Provider: Amazon Titan Embeddings (Amazon Bedrock)
SDK: boto3
Auth: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
"""

from __future__ import annotations

import os
from typing import Optional

from model_client import get_bedrock_runtime_client


# Provider-specific Amazon Titan Embeddings model IDs
TITAN_EMBEDDINGS_MODEL_V1 = "amazon.titan-embed-text-v1"
TITAN_EMBEDDINGS_MODEL_V2 = "amazon.titan-embed-text-v2:0"

DEFAULT_EMBEDDINGS_MODEL = TITAN_EMBEDDINGS_MODEL_V2


def generate_embedding(
    text: str,
    model_id: Optional[str] = None,
    region: Optional[str] = None,
    normalize: bool = True,
) -> dict:
    """Generate an embedding vector for text using Amazon Titan Embeddings.

    Provider signals: boto3 bedrock-runtime invoke_model, Amazon Titan model
    identifiers (amazon.titan-embed-text-v2:0), Bedrock-specific request body
    with inputText, dimensions, normalize parameters.

    Returns dict with embedding vector and metadata.
    """
    client = get_bedrock_runtime_client(region_name=region)
    resolved_model = model_id or DEFAULT_EMBEDDINGS_MODEL

    # Amazon Titan Embeddings v2 request body format
    body = {
        "inputText": text,
        "normalize": normalize,
    }

    # For v2 model, we can specify dimensions
    if resolved_model == TITAN_EMBEDDINGS_MODEL_V2:
        body["dimensions"] = 1024

    import json
    response = client.invoke_model(
        modelId=resolved_model,
        body=json.dumps(body),
    )

    import json as json_mod
    response_body = json_mod.loads(response.get("body").read())

    embedding = response_body.get("embedding", [])

    return {
        "embedding": embedding,
        "dimension": len(embedding),
        "model_id": resolved_model,
        "provider": "amazon-bedrock-titan-embeddings",
        "text_length": len(text),
        "normalized": normalize,
    }


def generate_embeddings_batch(
    texts: list[str],
    model_id: Optional[str] = None,
    region: Optional[str] = None,
    normalize: bool = True,
) -> list[dict]:
    """Generate embeddings for multiple texts using Amazon Titan Embeddings.

    Provider: Amazon Bedrock Titan Embeddings via boto3.
    """
    results = []
    for text in texts:
        result = generate_embedding(
            text=text,
            model_id=model_id,
            region=region,
            normalize=normalize,
        )
        results.append(result)
    return results


def compute_cosine_similarity(
    vec_a: list[float],
    vec_b: list[float],
) -> float:
    """Compute cosine similarity between two embedding vectors.

    Used for evaluating Amazon Titan embeddings similarity.
    """
    import math

    if len(vec_a) != len(vec_b):
        raise ValueError("Vectors must have the same dimension")

    dot_product = sum(a * b for a, b in zip(vec_a, vec_b))
    norm_a = math.sqrt(sum(a * a for a in vec_a))
    norm_b = math.sqrt(sum(b * b for b in vec_b))

    if norm_a == 0 or norm_b == 0:
        return 0.0

    return dot_product / (norm_a * norm_b)


def embed_platform_outputs(
    outputs: list[str],
    model_id: Optional[str] = None,
    region: Optional[str] = None,
) -> list[dict]:
    """Embed a list of platform model outputs for evaluation or retrieval.

    Provider: Amazon Titan Embeddings (amazon.titan-embed-text-v2:0) via
    Amazon Bedrock boto3 runtime.
    """
    return generate_embeddings_batch(
        texts=outputs,
        model_id=model_id,
        region=region,
        normalize=True,
    )


def get_embedding_model_info(model_id: Optional[str] = None) -> dict:
    """Return information about the Amazon Titan Embeddings model.

    Provider-specific: Amazon Titan model details.
    """
    resolved = model_id or DEFAULT_EMBEDDINGS_MODEL
    info = {
        TITAN_EMBEDDINGS_MODEL_V1: {
            "name": "Titan Embeddings G1 - Text",
            "dimension": 1536,
            "max_input_tokens": 8192,
        },
        TITAN_EMBEDDINGS_MODEL_V2: {
            "name": "Titan Embeddings Text V2",
            "dimension": 1024,
            "max_input_tokens": 8192,
        },
    }
    return info.get(resolved, {"model_id": resolved, "dimension": "unknown"})
