"""Embed platform outputs for evaluation or retrieval using Amazon Titan Embeddings.

Uses the boto3 bedrock-runtime invoke_model API with the
amazon.titan-embed-text-v2:0 model to generate vector embeddings
from text produced by a platform model.
Auth: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
Provider: Amazon Bedrock (Titan Embeddings)
"""

import json
from typing import List, Optional

from model_client import get_bedrock_runtime_client
from model_models import EmbeddingResult

TITAN_EMBED_MODEL_ID = "amazon.titan-embed-text-v2:0"


def platform_output_embedding(
    text: str,
    model_id: str = TITAN_EMBED_MODEL_ID,
    dimensions: Optional[int] = None,
    aws_access_key_id: Optional[str] = None,
    aws_secret_access_key: Optional[str] = None,
) -> EmbeddingResult:
    """Generate embeddings for platform model output using Amazon Titan.

    Calls the bedrock-runtime invoke_model API with
    amazon.titan-embed-text-v2:0 to produce a dense vector
    representation suitable for semantic search, retrieval, or
    similarity evaluation.
    """
    if not text or not text.strip():
        raise ValueError("Cannot embed empty text")

    client = get_bedrock_runtime_client(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
    )

    body: dict = {
        "inputText": text,
    }
    if dimensions is not None:
        body["dimensions"] = dimensions

    response = client.invoke_model(
        modelId=model_id,
        body=json.dumps(body),
        contentType="application/json",
        accept="application/json",
    )

    response_body = json.loads(response["body"].read())

    embedding_vector = response_body.get("embedding", [])
    input_tokens = response_body.get("inputTextTokenCount", 0)

    return EmbeddingResult(
        vector=embedding_vector,
        input_tokens=input_tokens,
        model_id=model_id,
        raw_response=response_body,
    )


def embed_multiple_outputs(
    texts: List[str],
    model_id: str = TITAN_EMBED_MODEL_ID,
    dimensions: Optional[int] = None,
    aws_access_key_id: Optional[str] = None,
    aws_secret_access_key: Optional[str] = None,
) -> List[EmbeddingResult]:
    """Generate embeddings for multiple platform outputs."""
    results: List[EmbeddingResult] = []
    for text in texts:
        if text and text.strip():
            result = platform_output_embedding(
                text=text,
                model_id=model_id,
                dimensions=dimensions,
                aws_access_key_id=aws_access_key_id,
                aws_secret_access_key=aws_secret_access_key,
            )
            results.append(result)
    return results


def cosine_similarity(vec_a: List[float], vec_b: List[float]) -> float:
    """Compute cosine similarity between two embedding vectors."""
    if len(vec_a) != len(vec_b):
        raise ValueError("Vectors must have the same dimensionality")

    dot_product = sum(a * b for a, b in zip(vec_a, vec_b))
    norm_a = sum(a * a for a in vec_a) ** 0.5
    norm_b = sum(b * b for b in vec_b) ** 0.5

    if norm_a == 0 or norm_b == 0:
        return 0.0

    return dot_product / (norm_a * norm_b)


if __name__ == "__main__":
    sample = "Machine learning models process natural language to generate responses."
    result = platform_output_embedding(sample)
    print(f"Model: {result.model_id}")
    print(f"Input tokens: {result.input_tokens}")
    print(f"Vector dimension: {len(result.vector)}")
    print(f"First 5 values: {result.vector[:5]}")
