"""
[LATER-STEP] crypto_audit_embedding.py

Embeds crypto audit notes for semantic search using Amazon Titan Embeddings
via Amazon Bedrock Runtime.
Provider: Amazon Bedrock Runtime (Titan Embeddings) | SDK: boto3 | Auth: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY

Uses the titan-embed-text-v1 model to generate embeddings of audit notes,
enabling semantic search over encryption/compliance documentation.
"""

import os
import sys
import json
import logging
from typing import Dict, List, Optional

import boto3
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)

# Amazon Titan Embedding model identifier
TITAN_EMBED_MODEL_ID = "amazon.titan-embed-text-v1:0"


def _build_bedrock_runtime_client() -> boto3.client:
    """Build an Amazon Bedrock Runtime client using environment credentials."""
    return boto3.client(
        "bedrock-runtime",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_DEFAULT_REGION", "us-east-1"),
    )


def embed_text(
    text: str,
    model_id: str = TITAN_EMBED_MODEL_ID,
) -> List[float]:
    """
    Generate an embedding vector for a text string using Amazon Titan Embeddings.

    Args:
        text: Text content to embed.
        model_id: Bedrock model identifier (default: amazon.titan-embed-text-v1:0).

    Returns:
        List of floats representing the embedding vector.

    Raises:
        RuntimeError: If the Bedrock invoke call fails.
    """
    client = _build_bedrock_runtime_client()

    body = json.dumps({"inputText": text})

    try:
        response = client.invoke_model(
            modelId=model_id,
            contentType="application/json",
            accept="application/json",
            body=body,
        )
    except ClientError as exc:
        logger.error("Bedrock embedding failed: %s", exc)
        raise RuntimeError(f"Bedrock embedding invocation failed: {exc}") from exc

    response_body = json.loads(response["body"].read().decode("utf-8"))
    return response_body.get("embedding", [])


def embed_audit_notes(
    notes: List[str],
    model_id: str = TITAN_EMBED_MODEL_ID,
) -> List[Dict]:
    """
    Embed a list of crypto audit notes and return structured results.

    Args:
        notes: List of audit note strings to embed.
        model_id: Bedrock model identifier.

    Returns:
        List of dicts with 'index', 'note', and 'embedding' keys.
    """
    results = []
    for idx, note in enumerate(notes):
        if not note or not note.strip():
            continue
        try:
            embedding = embed_text(note.strip(), model_id=model_id)
            results.append({
                "index": idx,
                "note": note,
                "embedding": embedding,
                "model_id": model_id,
            })
        except RuntimeError as exc:
            logger.warning("Failed to embed note at index %d: %s", idx, exc)
            results.append({
                "index": idx,
                "note": note,
                "embedding": [],
                "error": str(exc),
                "model_id": model_id,
            })
    return results


def search_similar_notes(
    query: str,
    embedded_notes: List[Dict],
    top_k: int = 5,
) -> List[Dict]:
    """
    Search for the most similar audit notes to a query using cosine similarity.

    Args:
        query: Query text to embed and compare.
        embedded_notes: List of previously embedded note dicts.
        top_k: Number of top results to return.

    Returns:
        List of note dicts sorted by similarity score (descending).
    """
    query_embedding = embed_text(query)
    if not query_embedding:
        return []

    scored = []
    for note_entry in embedded_notes:
        vec = note_entry.get("embedding", [])
        if not vec or "error" in note_entry:
            continue
        similarity = _cosine_similarity(query_embedding, vec)
        scored.append({
            "index": note_entry["index"],
            "note": note_entry["note"],
            "similarity": similarity,
            "model_id": note_entry.get("model_id", TITAN_EMBED_MODEL_ID),
        })

    scored.sort(key=lambda x: x["similarity"], reverse=True)
    return scored[:top_k]


def _cosine_similarity(vec_a: List[float], vec_b: List[float]) -> float:
    """Compute cosine similarity between two vectors."""
    if len(vec_a) != len(vec_b) or not vec_a:
        return 0.0
    dot = sum(a * b for a, b in zip(vec_a, vec_b))
    norm_a = sum(a * a for a in vec_a) ** 0.5
    norm_b = sum(b * b for b in vec_b) ** 0.5
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


def embed_crypto_audit_notes(
    notes: List[str],
    model_id: str = TITAN_EMBED_MODEL_ID,
) -> List[Dict]:
    """
    High-level function to embed crypto audit notes using Titan Embeddings.

    Args:
        notes: Audit note strings.
        model_id: Bedrock model identifier.

    Returns:
        List of embedded note results.
    """
    return embed_audit_notes(notes, model_id=model_id)


def main() -> None:
    """CLI entry point for embedding audit notes."""
    logging.basicConfig(level=logging.INFO)

    notes = []
    if len(sys.argv) > 1:
        notes = [sys.argv[1]]
    else:
        notes = sys.stdin.read().strip().split("\n")

    if not notes:
        print("Error: No notes provided.", file=sys.stderr)
        sys.exit(1)

    results = embed_crypto_audit_notes([n for n in notes if n.strip()])
    for r in results:
        emb = r.get("embedding", [])
        print(f"Note {r['index']}: embedding size={len(emb)}, error={'error' in r}")


if __name__ == "__main__":
    main()
