"""
crypto_audit_embedding.py - Embeds crypto audit notes for semantic search using Amazon Bedrock.

Uses Amazon Bedrock with Amazon Titan Text Embeddings V2 (amazon.titan-embed-text-v2:0)
to generate vector embeddings of cryptographic audit notes. These embeddings can be
stored in a vector database (e.g., OpenSearch, Pinecone, FAISS) for semantic search
and similarity matching.

Provider: Amazon Bedrock (bedrock.us-east-1.amazonaws.com)
Model ID: amazon.titan-embed-text-v2:0 (1024-dimensional embeddings)
"""

import json
import logging
import sys
from typing import Any, Dict, List, Optional

import boto3
from botocore.config import Config

from security_models import AuditEmbedding

logger = logging.getLogger(__name__)

REGION = "us-east-1"
EMBEDDING_MODEL_ID = "amazon.titan-embed-text-v2:0"
DEFAULT_DIMENSIONS = 1024


def get_bedrock_runtime_client(region: str = REGION) -> boto3.client:
    """
    Initialize an Amazon Bedrock Runtime client via boto3.
    Endpoint: bedrock-runtime.us-east-1.amazonaws.com
    """
    config = Config(
        retries={"max_attempts": 3, "mode": "adaptive"},
        region_name=region,
    )
    return boto3.client("bedrock-runtime", config=config)


def generate_embedding(
    text: str,
    model_id: str = EMBEDDING_MODEL_ID,
    region: str = REGION,
    dimensions: int = DEFAULT_DIMENSIONS,
) -> List[float]:
    """
    Generate a vector embedding for text using Amazon Titan Embeddings V2 on Bedrock.

    Args:
        text: The audit note text to embed.
        model_id: Bedrock model ID (default: amazon.titan-embed-text-v2:0).
        region: AWS region for Bedrock.
        dimensions: Output embedding dimensions (1024 for Titan V2 default).

    Returns:
        List of floats representing the embedding vector.

    Raises:
        RuntimeError: If Bedrock embedding generation fails.
    """
    client = get_bedrock_runtime_client(region)

    try:
        response = client.invoke_model(
            modelId=model_id,
            body=json.dumps({
                "inputText": text,
                "dimensions": dimensions,
                "normalize": True,
            }),
        )

        body = json.loads(response["body"].read().decode("utf-8"))
        embedding = body.get("embedding", [])

        if not embedding:
            raise RuntimeError(f"No embedding returned from model {model_id}")

        logger.info(
            "Generated embedding with %s: %d dimensions",
            model_id,
            len(embedding),
        )
        return embedding

    except Exception as e:
        raise RuntimeError(
            f"Amazon Bedrock embedding failed with model {model_id}: {e}"
        ) from e


def embed_audit_note(
    audit_note: str,
    model_id: str = EMBEDDING_MODEL_ID,
    region: str = REGION,
    dimensions: int = DEFAULT_DIMENSIONS,
    metadata: Optional[Dict[str, Any]] = None,
) -> AuditEmbedding:
    """
    Create an embedded audit note for semantic search.

    Args:
        audit_note: The cryptographic audit note text to embed.
        model_id: Bedrock model ID.
        region: AWS region.
        dimensions: Embedding vector dimensions.
        metadata: Additional metadata (key_id, date, auditor, etc.).

    Returns:
        AuditEmbedding with the note, embedding vector, and model info.

    Raises:
        RuntimeError: If embedding generation fails.
    """
    embedding = generate_embedding(audit_note, model_id=model_id, region=region, dimensions=dimensions)

    result = AuditEmbedding(
        audit_note=audit_note,
        embedding=embedding,
        model=model_id,
        dimensions=len(embedding),
        metadata=metadata or {},
    )

    logger.info(
        "Embedded audit note with model %s: %d dimensions",
        model_id,
        result.dimensions,
    )
    return result


def embed_multiple_audit_notes(
    notes: List[str],
    model_id: str = EMBEDDING_MODEL_ID,
    region: str = REGION,
    dimensions: int = DEFAULT_DIMENSIONS,
    metadata_list: Optional[List[Dict[str, Any]]] = None,
) -> List[AuditEmbedding]:
    """
    Embed multiple audit notes for batch semantic search indexing.

    Args:
        notes: List of audit note strings.
        model_id: Bedrock model ID.
        region: AWS region.
        dimensions: Embedding dimensions.
        metadata_list: Optional list of metadata dicts per note.

    Returns:
        List of AuditEmbedding objects.
    """
    results = []
    for i, note in enumerate(notes):
        meta = metadata_list[i] if metadata_list and i < len(metadata_list) else {}
        result = embed_audit_note(
            note,
            model_id=model_id,
            region=region,
            dimensions=dimensions,
            metadata=meta,
        )
        results.append(result)
    return results


def main():
    """CLI entry point for crypto_audit_embedding."""
    if len(sys.argv) < 2:
        print("Usage: python crypto_audit_embedding.py <audit_note_text>")
        sys.exit(1)

    audit_note = sys.argv[1]

    logging.basicConfig(level=logging.INFO)
    result = embed_audit_note(audit_note)

    output = {
        "audit_note": result.audit_note,
        "model": result.model,
        "dimensions": result.dimensions,
        "embedding_preview": result.embedding[:10],
        "metadata": result.metadata,
    }
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
