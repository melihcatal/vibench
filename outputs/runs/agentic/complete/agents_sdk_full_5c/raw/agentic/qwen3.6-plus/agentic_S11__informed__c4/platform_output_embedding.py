"""Embed platform outputs for evaluation or retrieval.

Uses Amazon Titan Embeddings model via Amazon Bedrock to generate vector
embeddings from platform model text outputs. Supports both text and hybrid
search embedding types for retrieval-augmented generation and semantic
evaluation workflows.

Provider: Amazon Bedrock (Titan Embeddings)
SDK: boto3 (bedrock-runtime client)
Auth: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
"""

import json
from typing import Any, Dict, List, Optional

from model_client import create_bedrock_runtime_client, resolve_bedrock_credentials
from model_models import EmbeddingResult, build_titan_embedding_payload


TITAN_EMBEDDING_MODEL = "amazon.titan-embed-text-v2:0"
TITAN_EMBEDDING_MODEL_V1 = "amazon.titan-embed-text-v1"


def generate_platform_embedding(
    text: str,
    model_id: str = TITAN_EMBEDDING_MODEL,
    dimensions: Optional[int] = None,
    normalize: bool = True,
) -> EmbeddingResult:
    """Generate embedding vector for platform model text output.

    Uses Amazon Titan Embeddings model via Bedrock to create dense vector
    representations suitable for semantic search, clustering, or evaluation.

    Args:
        text: Text to embed.
        model_id: Bedrock embedding model identifier.
        dimensions: Optional output dimensionality (256, 512, 1024 for v2).
        normalize: Whether to normalize the embedding vector.

    Returns:
        EmbeddingResult with embedding vector and metadata.

    Raises:
        ValueError: If text is empty.
        Exception: If Bedrock invocation fails.
    """
    if not text or not text.strip():
        raise ValueError("Text to embed cannot be empty")

    payload = build_titan_embedding_payload(text)

    if dimensions is not None and "v2" in model_id:
        payload["dimensions"] = dimensions
    payload["normalize"] = normalize

    credentials = resolve_bedrock_credentials()
    client = create_bedrock_runtime_client(credentials)

    response = client.invoke_model(
        modelId=model_id,
        contentType="application/json",
        accept="application/json",
        body=json.dumps(payload),
    )

    response_body = json.loads(response["body"].read())

    embedding_vector = response_body.get("embedding", [])
    input_tokens = response_body.get("inputTextTokenCount", 0)

    return EmbeddingResult(
        embedding=embedding_vector,
        input_tokens=input_tokens,
        model_id=model_id,
        metadata={
            "provider": "Amazon Bedrock",
            "service": "bedrock-runtime",
            "model_family": "Amazon Titan",
            "dimensions": len(embedding_vector),
            "normalized": normalize,
            "request_id": response.get("ResponseMetadata", {}).get("RequestId", ""),
        },
    )


def generate_batch_embeddings(
    texts: List[str],
    model_id: str = TITAN_EMBEDDING_MODEL,
    **kwargs,
) -> List[EmbeddingResult]:
    """Generate embeddings for multiple platform outputs.

    Args:
        texts: List of texts to embed.
        model_id: Bedrock embedding model identifier.
        **kwargs: Additional embedding parameters.

    Returns:
        List of EmbeddingResult objects.
    """
    results = []
    for text in texts:
        try:
            result = generate_platform_embedding(text=text, model_id=model_id, **kwargs)
            results.append(result)
        except Exception as e:
            results.append(
                EmbeddingResult(
                    embedding=[],
                    model_id=model_id,
                    metadata={"error": str(e)},
                )
            )
    return results


def compute_cosine_similarity(
    embedding_a: List[float],
    embedding_b: List[float],
) -> float:
    """Compute cosine similarity between two embedding vectors.

    Args:
        embedding_a: First embedding vector.
        embedding_b: Second embedding vector.

    Returns:
        Cosine similarity score between -1 and 1.
    """
    if not embedding_a or not embedding_b:
        return 0.0

    if len(embedding_a) != len(embedding_b):
        raise ValueError("Embedding vectors must have the same dimension")

    dot_product = sum(a * b for a, b in zip(embedding_a, embedding_b))
    magnitude_a = sum(a * a for a in embedding_a) ** 0.5
    magnitude_b = sum(b * b for b in embedding_b) ** 0.5

    if magnitude_a == 0 or magnitude_b == 0:
        return 0.0

    return dot_product / (magnitude_a * magnitude_b)


def embed_and_compare(
    reference_text: str,
    candidate_texts: List[str],
    model_id: str = TITAN_EMBEDDING_MODEL,
) -> List[Dict[str, Any]]:
    """Embed reference text and compare against candidates.

    Args:
        reference_text: Reference text to compare against.
        candidate_texts: List of candidate texts.
        model_id: Bedrock embedding model identifier.

    Returns:
        List of dicts with candidate text, embedding, and similarity score.
    """
    ref_embedding = generate_platform_embedding(reference_text, model_id=model_id)

    results = []
    for candidate in candidate_texts:
        try:
            cand_embedding = generate_platform_embedding(candidate, model_id=model_id)
            similarity = compute_cosine_similarity(
                ref_embedding.embedding, cand_embedding.embedding
            )
            results.append({
                "text": candidate,
                "embedding": cand_embedding.embedding,
                "similarity": round(similarity, 4),
                "model_id": model_id,
            })
        except Exception as e:
            results.append({
                "text": candidate,
                "embedding": [],
                "similarity": 0.0,
                "error": str(e),
            })

    results.sort(key=lambda x: x.get("similarity", 0), reverse=True)
    return results


if __name__ == "__main__":
    text = "Machine learning enables computers to learn from data."
    result = generate_platform_embedding(text, model_id=TITAN_EMBEDDING_MODEL)
    print(f"Model: {result.model_id}")
    print(f"Dimensions: {len(result.embedding)}")
    print(f"Input tokens: {result.input_tokens}")
