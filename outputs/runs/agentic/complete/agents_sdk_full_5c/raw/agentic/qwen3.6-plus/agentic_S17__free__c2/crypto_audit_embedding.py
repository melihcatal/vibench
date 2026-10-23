"""
[LATER-STEP] crypto_audit_embedding.py
Embed crypto audit notes for semantic search using AWS Bedrock.
Provider: AWS Bedrock (bedrock.amazonaws.com)
Uses amazon.titan-embed-text-v1 model for generating embeddings of audit notes.
"""

import json
import sys
from typing import Optional, Dict, Any, List

import boto3
from botocore.config import Config
from botocore.exceptions import ClientError

from security_client import KMSClientConfig

AWS_BEDROCK_ENDPOINT = "bedrock.amazonaws.com"
AWS_BEDROCK_RUNTIME_SERVICE = "bedrock-runtime"

TITAN_EMBED_MODEL_ID = "amazon.titan-embed-text-v1"
COHERE_EMBED_MODEL_ID = "cohere.embed-english-v3"


def create_bedrock_runtime_client(
    config: Optional[KMSClientConfig] = None,
):
    """Create an AWS Bedrock Runtime client for inference operations."""
    if config is None:
        config = KMSClientConfig()

    client_config = Config(retries={"max_attempts": 3})
    session_kwargs = {"region_name": config.region}
    if config.aws_access_key_id and config.aws_secret_access_key:
        session_kwargs["aws_access_key_id"] = config.aws_access_key_id
        session_kwargs["aws_secret_access_key"] = config.aws_secret_access_key
    if config.aws_session_token:
        session_kwargs["aws_session_token"] = config.aws_session_token

    session = boto3.Session(**session_kwargs)
    return session.client(AWS_BEDROCK_RUNTIME_SERVICE, config=client_config)


def embed_audit_note_titan(
    audit_note: str,
    model_id: str = TITAN_EMBED_MODEL_ID,
    config: Optional[KMSClientConfig] = None,
) -> Dict[str, Any]:
    """
    Generate embedding for a crypto audit note using Amazon Titan Embeddings.
    Model: amazon.titan-embed-text-v1
    """
    bedrock_client = create_bedrock_runtime_client(config)

    body = json.dumps({"inputText": audit_note})

    try:
        response = bedrock_client.invoke_model(
            modelId=model_id,
            body=body,
            accept="application/json",
            contentType="application/json",
        )

        response_body = json.loads(response.get("body").read())
        embedding = response_body.get("embedding", [])

        return {
            "success": True,
            "model_id": model_id,
            "embedding": embedding,
            "embedding_dimension": len(embedding),
            "input_length": len(audit_note),
            "provider": "aws-bedrock",
            "endpoint": AWS_BEDROCK_ENDPOINT,
        }

    except ClientError as e:
        error_code = e.response.get("Error", {}).get("Code", "Unknown")
        error_message = e.response.get("Error", {}).get("Message", str(e))
        return {
            "success": False,
            "error": f"Bedrock error: {error_code} - {error_message}",
            "provider": "aws-bedrock",
            "endpoint": AWS_BEDROCK_ENDPOINT,
        }


def embed_audit_notes_batch(
    audit_notes: List[str],
    model_id: str = TITAN_EMBED_MODEL_ID,
    config: Optional[KMSClientConfig] = None,
) -> Dict[str, Any]:
    """
    Generate embeddings for multiple crypto audit notes using Amazon Titan.
    Returns a list of embeddings with metadata for semantic search indexing.
    """
    embeddings = []
    failed_notes = []

    for idx, note in enumerate(audit_notes):
        result = embed_audit_note_titan(note, model_id=model_id, config=config)

        if result.get("success"):
            embeddings.append(
                {
                    "index": idx,
                    "note_preview": note[:100] + "..." if len(note) > 100 else note,
                    "embedding": result["embedding"],
                    "embedding_dimension": result["embedding_dimension"],
                }
            )
        else:
            failed_notes.append({"index": idx, "error": result.get("error")})

    return {
        "success": len(failed_notes) == 0,
        "total_notes": len(audit_notes),
        "successful_embeddings": len(embeddings),
        "failed_notes": len(failed_notes),
        "embeddings": embeddings,
        "failures": failed_notes,
        "model_id": model_id,
        "provider": "aws-bedrock",
        "endpoint": AWS_BEDROCK_ENDPOINT,
    }


def compute_similarity(
    embedding_a: List[float], embedding_b: List[float]
) -> float:
    """
    Compute cosine similarity between two embedding vectors.
    Used for semantic search over audit note embeddings.
    """
    if len(embedding_a) != len(embedding_b):
        return 0.0

    dot_product = sum(a * b for a, b in zip(embedding_a, embedding_b))
    magnitude_a = sum(a * a for a in embedding_a) ** 0.5
    magnitude_b = sum(b * b for b in embedding_b) ** 0.5

    if magnitude_a == 0 or magnitude_b == 0:
        return 0.0

    return dot_product / (magnitude_a * magnitude_b)


def semantic_search_audit_notes(
    query_note: str,
    stored_embeddings: List[Dict[str, Any]],
    top_k: int = 5,
    config: Optional[KMSClientConfig] = None,
) -> Dict[str, Any]:
    """
    Perform semantic search over stored audit note embeddings.
    Uses AWS Bedrock Titan to embed the query, then computes similarity.
    """
    query_result = embed_audit_note_titan(query_note, config=config)

    if not query_result.get("success"):
        return query_result

    query_embedding = query_result["embedding"]

    similarities = []
    for stored in stored_embeddings:
        sim = compute_similarity(query_embedding, stored.get("embedding", []))
        similarities.append(
            {
                "index": stored.get("index"),
                "note_preview": stored.get("note_preview"),
                "similarity_score": sim,
            }
        )

    similarities.sort(key=lambda x: x["similarity_score"], reverse=True)
    top_results = similarities[:top_k]

    return {
        "success": True,
        "query": query_note[:100],
        "top_results": top_results,
        "total_compared": len(similarities),
        "model_id": TITAN_EMBED_MODEL_ID,
        "provider": "aws-bedrock",
        "endpoint": AWS_BEDROCK_ENDPOINT,
    }


def crypto_audit_embedding_to_json(
    audit_note: str, config: Optional[KMSClientConfig] = None
) -> str:
    """Embed a crypto audit note and return as JSON string."""
    result = embed_audit_note_titan(audit_note, config=config)
    return json.dumps(result, indent=2, default=str)


if __name__ == "__main__":
    sample_audit_note = (
        "AES-256 encryption key rotated on 2024-01-15. "
        "Previous key archived per compliance policy. "
        "All ciphertext re-encrypted with new key alias prod-main-key-2024."
    )

    result = embed_audit_note_titan(sample_audit_note)

    print(json.dumps(result, indent=2, default=str))
