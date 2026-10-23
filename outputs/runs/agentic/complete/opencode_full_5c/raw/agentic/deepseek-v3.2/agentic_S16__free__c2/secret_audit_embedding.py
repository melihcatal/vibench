import openai
import os
import json
from typing import List, Dict, Any, Optional
from datetime import datetime


def embed_secret_audit_notes(secret_name: str, audit_notes: str) -> Dict[str, Any]:
    """
    Embed secret audit notes for semantic search using OpenAI's embedding API.

    Args:
        secret_name: Name of the secret
        audit_notes: Audit notes text to embed

    Returns:
        Dictionary with embedding and metadata
    """
    # Initialize OpenAI client
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise Exception("OPENAI_API_KEY environment variable is required")

    openai.api_key = api_key

    try:
        # Create embedding using OpenAI's text-embedding-ada-002 model
        response = openai.Embedding.create(
            model="text-embedding-ada-002", input=audit_notes, encoding_format="float"
        )

        embedding = response["data"][0]["embedding"]

        # Create metadata
        metadata = {
            "secret_name": secret_name,
            "audit_timestamp": datetime.utcnow().isoformat() + "Z",
            "embedding_model": "text-embedding-ada-002",
            "embedding_dimensions": len(embedding),
            "notes_length": len(audit_notes),
            "notes_preview": audit_notes[:100] + "..."
            if len(audit_notes) > 100
            else audit_notes,
        }

        result = {
            "embedding": embedding,
            "metadata": metadata,
            "raw_response": {
                "model": response["model"],
                "usage": dict(response["usage"]),
                "object": response["object"],
            },
        }

        return result

    except openai.error.AuthenticationError:
        raise Exception("OpenAI authentication failed. Check your API key.")
    except openai.error.RateLimitError:
        raise Exception("OpenAI rate limit exceeded. Please try again later.")
    except openai.error.APIError as e:
        raise Exception(f"OpenAI API error: {e}")
    except Exception as e:
        raise Exception(f"Failed to create embedding: {e}")


def batch_embed_audit_notes(
    audit_records: List[Dict[str, str]],
) -> List[Dict[str, Any]]:
    """
    Batch embed multiple audit notes.

    Args:
        audit_records: List of dictionaries with 'secret_name' and 'audit_notes'

    Returns:
        List of embedding results
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise Exception("OPENAI_API_KEY environment variable is required")

    openai.api_key = api_key

    # Prepare inputs for batch processing
    inputs = [record["audit_notes"] for record in audit_records]

    try:
        response = openai.Embedding.create(
            model="text-embedding-ada-002", input=inputs, encoding_format="float"
        )

        results = []
        for i, embedding_data in enumerate(response["data"]):
            record = audit_records[i]
            embedding = embedding_data["embedding"]

            metadata = {
                "secret_name": record["secret_name"],
                "audit_timestamp": datetime.utcnow().isoformat() + "Z",
                "embedding_model": "text-embedding-ada-002",
                "embedding_dimensions": len(embedding),
                "notes_length": len(record["audit_notes"]),
                "notes_preview": record["audit_notes"][:100] + "..."
                if len(record["audit_notes"]) > 100
                else record["audit_notes"],
            }

            results.append({"embedding": embedding, "metadata": metadata})

        return results

    except Exception as e:
        raise Exception(f"Failed to batch embed audit notes: {e}")


def search_similar_audits(
    query: str, embeddings_db: List[Dict[str, Any]], top_k: int = 5
) -> List[Dict[str, Any]]:
    """
    Search for similar audit notes using cosine similarity.

    Args:
        query: Search query text
        embeddings_db: List of embedding results from embed_secret_audit_notes
        top_k: Number of top results to return

    Returns:
        List of similar audit results with similarity scores
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise Exception("OPENAI_API_KEY environment variable is required")

    openai.api_key = api_key

    try:
        # Embed the query
        query_response = openai.Embedding.create(
            model="text-embedding-ada-002", input=query, encoding_format="float"
        )
        query_embedding = query_response["data"][0]["embedding"]

        # Calculate cosine similarities
        import numpy as np

        similarities = []
        for item in embeddings_db:
            embedding = item["embedding"]

            # Convert to numpy arrays for efficient calculation
            query_vec = np.array(query_embedding)
            doc_vec = np.array(embedding)

            # Calculate cosine similarity
            similarity = np.dot(query_vec, doc_vec) / (
                np.linalg.norm(query_vec) * np.linalg.norm(doc_vec)
            )

            similarities.append(
                {
                    "similarity": float(similarity),
                    "metadata": item["metadata"],
                    "embedding": embedding,  # Keep for potential further processing
                }
            )

        # Sort by similarity (descending)
        similarities.sort(key=lambda x: x["similarity"], reverse=True)

        # Return top-k results
        return similarities[:top_k]

    except Exception as e:
        raise Exception(f"Failed to search similar audits: {e}")


def create_audit_embedding_storage(
    secret_name: str, audit_data: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Create a complete audit embedding storage record.

    Args:
        secret_name: Name of the secret
        audit_data: Audit data including notes, auditor, findings, etc.

    Returns:
        Complete embedding storage record
    """
    # Extract audit notes from audit data
    audit_notes = audit_data.get("notes", "")
    if not audit_notes:
        audit_notes = json.dumps(audit_data, indent=2)

    # Create embedding
    embedding_result = embed_secret_audit_notes(secret_name, audit_notes)

    # Create comprehensive storage record
    storage_record = {
        "id": f"audit_{secret_name}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
        "secret_name": secret_name,
        "audit_data": audit_data,
        "embedding": embedding_result["embedding"],
        "embedding_metadata": embedding_result["metadata"],
        "created_at": datetime.utcnow().isoformat() + "Z",
        "version": "1.0",
    }

    return storage_record


if __name__ == "__main__":
    # Example usage
    audit_notes = "Secret rotated on 2024-01-15. New version deployed to production. Old version archived. Rotation triggered by automated schedule."

    try:
        embedding_result = embed_secret_audit_notes("prod/api-key", audit_notes)
        print(f"Embedding created for {embedding_result['metadata']['secret_name']}")
        print(f"Dimensions: {embedding_result['metadata']['embedding_dimensions']}")
        print(f"Model: {embedding_result['metadata']['embedding_model']}")
    except Exception as e:
        print(f"Error: {e}")
