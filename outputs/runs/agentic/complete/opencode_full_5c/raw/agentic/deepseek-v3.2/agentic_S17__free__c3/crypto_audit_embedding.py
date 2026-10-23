import os
import json
from typing import Dict, List, Any, Optional
import boto3
from botocore.exceptions import ClientError
import numpy as np


def embed_crypto_audit_notes(notes_text, model_id=None):
    """
    Embed crypto audit notes for semantic search using AWS Bedrock.

    Args:
        notes_text: Audit notes text to embed
        model_id: Bedrock model ID for embeddings

    Returns:
        dict with embedding and metadata
    """
    if model_id is None:
        model_id = os.environ.get(
            "AWS_BEDROCK_EMBEDDING_MODEL", "amazon.titan-embed-text-v1"
        )

    if isinstance(notes_text, str):
        notes_text = [notes_text]

    bedrock_client = boto3.client(
        "bedrock-runtime", region_name=os.environ.get("AWS_REGION", "us-east-1")
    )

    try:
        embeddings = []
        for text in notes_text:
            if len(text) > 10000:
                text = text[:10000]

            if model_id.startswith("amazon.titan"):
                request_body = {"inputText": text}

                response = bedrock_client.invoke_model(
                    modelId=model_id, body=json.dumps(request_body)
                )

                response_body = json.loads(response["body"].read())
                embedding = response_body.get("embedding", [])

            elif model_id.startswith("cohere"):
                request_body = {"texts": [text], "input_type": "search_document"}

                response = bedrock_client.invoke_model(
                    modelId=model_id, body=json.dumps(request_body)
                )

                response_body = json.loads(response["body"].read())
                embedding = response_body.get("embeddings", [[]])[0]

            else:
                raise ValueError(f"Unsupported model: {model_id}")

            embeddings.append(
                {
                    "text": text[:500] + ("..." if len(text) > 500 else ""),
                    "embedding": embedding,
                    "embedding_dimensions": len(embedding),
                }
            )

        return {
            "embeddings": embeddings,
            "model_id": model_id,
            "total_texts": len(notes_text),
            "provider": "aws_bedrock",
        }

    except ClientError as e:
        raise Exception(f"AWS Bedrock embedding failed: {e}")


def search_similar_audit_notes(query_text, embeddings_data, top_k=5):
    """
    Search for similar audit notes using cosine similarity.

    Args:
        query_text: Query text to search for
        embeddings_data: Previous embeddings result
        top_k: Number of top results to return

    Returns:
        dict with search results
    """
    if "embeddings" not in embeddings_data:
        raise ValueError("Invalid embeddings data format")

    query_embedding_result = embed_crypto_audit_notes(
        query_text, embeddings_data["model_id"]
    )
    if not query_embedding_result["embeddings"]:
        raise ValueError("Failed to embed query text")

    query_embedding = query_embedding_result["embeddings"][0]["embedding"]
    query_vector = np.array(query_embedding)

    similarities = []
    for idx, item in enumerate(embeddings_data["embeddings"]):
        item_vector = np.array(item["embedding"])

        cosine_sim = np.dot(query_vector, item_vector) / (
            np.linalg.norm(query_vector) * np.linalg.norm(item_vector)
        )

        similarities.append(
            {
                "index": idx,
                "text": item["text"],
                "similarity": float(cosine_sim),
                "embedding_dimensions": item["embedding_dimensions"],
            }
        )

    similarities.sort(key=lambda x: x["similarity"], reverse=True)

    return {
        "query": query_text[:200] + ("..." if len(query_text) > 200 else ""),
        "model_id": embeddings_data["model_id"],
        "total_documents": len(embeddings_data["embeddings"]),
        "top_results": similarities[:top_k],
        "provider": "aws_bedrock",
    }


def create_audit_note_embedding_store(audit_notes, store_name=None):
    """
    Create a store of embedded audit notes for semantic search.

    Args:
        audit_notes: List of audit note texts
        store_name: Optional name for the store

    Returns:
        dict with embedding store
    """
    embedding_result = embed_crypto_audit_notes(audit_notes)

    store = {
        "name": store_name or "crypto_audit_notes",
        "created_at": json.dumps(os.environ.get("TIMESTAMP", "")),
        "model_id": embedding_result["model_id"],
        "embeddings": embedding_result["embeddings"],
        "total_notes": len(audit_notes),
        "provider": "aws_bedrock",
        "metadata": {
            "note_types": categorize_audit_notes(audit_notes),
            "avg_note_length": sum(len(note) for note in audit_notes) / len(audit_notes)
            if audit_notes
            else 0,
        },
    }

    return store


def categorize_audit_notes(notes):
    """Categorize audit notes based on content."""
    categories = {
        "key_management": 0,
        "encryption": 0,
        "compliance": 0,
        "incident": 0,
        "configuration": 0,
        "other": 0,
    }

    keywords = {
        "key_management": [
            "key",
            "rotation",
            "KMS",
            "HSM",
            "key material",
            "key policy",
        ],
        "encryption": ["encrypt", "decrypt", "cipher", "plaintext", "crypto", "AEAD"],
        "compliance": ["compliance", "audit", "PCI", "HIPAA", "GDPR", "SOX"],
        "incident": [
            "breach",
            "leak",
            "exposure",
            "incident",
            "response",
            "remediation",
        ],
        "configuration": ["config", "policy", "setting", "parameter", "environment"],
    }

    for note in notes:
        note_lower = note.lower()
        categorized = False

        for category, cat_keywords in keywords.items():
            for keyword in cat_keywords:
                if keyword.lower() in note_lower:
                    categories[category] += 1
                    categorized = True
                    break
            if categorized:
                break

        if not categorized:
            categories["other"] += 1

    return categories


def generate_audit_summary_from_embeddings(embedding_store, query_texts=None):
    """
    Generate an audit summary by analyzing embedded notes.

    Args:
        embedding_store: Store of embedded audit notes
        query_texts: Optional query texts to analyze against

    Returns:
        dict with audit summary
    """
    if query_texts is None:
        query_texts = [
            "key rotation compliance",
            "encryption configuration issues",
            "security incident response",
            "audit findings and remediation",
        ]

    search_results = []
    for query in query_texts:
        try:
            results = search_similar_audit_notes(query, embedding_store, top_k=3)
            search_results.append(
                {"query": query, "top_matches": results["top_results"]}
            )
        except Exception as e:
            search_results.append({"query": query, "error": str(e)})

    summary = {
        "store_name": embedding_store.get("name", "unknown"),
        "total_notes": embedding_store.get("total_notes", 0),
        "note_categories": embedding_store.get("metadata", {}).get("note_types", {}),
        "search_analysis": search_results,
        "model_used": embedding_store.get("model_id", "unknown"),
        "provider": embedding_store.get("provider", "aws_bedrock"),
        "summary_generated": json.dumps(os.environ.get("TIMESTAMP", "")),
    }

    return summary


def save_embedding_store_to_s3(embedding_store, bucket_name, key_prefix):
    """
    Save embedding store to S3 for persistence.

    Args:
        embedding_store: Embedding store to save
        bucket_name: S3 bucket name
        key_prefix: S3 key prefix

    Returns:
        dict with save result
    """
    s3_client = boto3.client(
        "s3", region_name=os.environ.get("AWS_REGION", "us-east-1")
    )

    try:
        key = f"{key_prefix}/{embedding_store['name']}_{json.dumps(os.environ.get('TIMESTAMP', ''))}.json"

        s3_client.put_object(
            Bucket=bucket_name,
            Key=key,
            Body=json.dumps(embedding_store, indent=2),
            ContentType="application/json",
        )

        return {
            "success": True,
            "bucket": bucket_name,
            "key": key,
            "store_name": embedding_store["name"],
            "provider": "aws_s3",
        }

    except ClientError as e:
        raise Exception(f"Failed to save embedding store to S3: {e}")


if __name__ == "__main__":
    test_notes = [
        "Key rotation completed for production KMS key on 2024-01-15",
        "Encryption configuration audit found weak cipher suites in TLS settings",
        "Incident response: Investigated potential key exposure, no evidence found",
        "Compliance check: All encryption meets PCI DSS requirements",
    ]

    embedding_result = embed_crypto_audit_notes(test_notes)
    print(f"Embedding result: {json.dumps(embedding_result, indent=2)}")
