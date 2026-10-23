import os
import numpy as np
from typing import List, Dict, Any
import openai


def embed_log_messages(
    messages: List[str], model: str = "text-embedding-3-small"
) -> Dict[str, Any]:
    """Embed selected log messages for semantic retrieval using OpenAI Embeddings API."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")

    # Initialize OpenAI client
    client = openai.OpenAI(api_key=api_key)

    if not messages:
        return {"embeddings": [], "model_used": model, "total_messages": 0}

    # Clean and prepare messages
    cleaned_messages = []
    for msg in messages:
        if isinstance(msg, str) and msg.strip():
            cleaned_messages.append(msg.strip())
        else:
            cleaned_messages.append(str(msg) if msg else "")

    try:
        # Call OpenAI Embeddings API
        response = client.embeddings.create(
            model=model, input=cleaned_messages, encoding_format="float"
        )

        # Extract embeddings
        embeddings = []
        for idx, data in enumerate(response.data):
            embedding_vector = data.embedding
            embeddings.append(
                {
                    "message": cleaned_messages[idx]
                    if idx < len(cleaned_messages)
                    else "",
                    "embedding": embedding_vector,
                    "index": data.index,
                    "embedding_id": data.id if hasattr(data, "id") else None,
                }
            )

        # Calculate statistics
        if embeddings:
            all_vectors = [e["embedding"] for e in embeddings]
            avg_vector = np.mean(all_vectors, axis=0).tolist()
            vector_dimension = len(embeddings[0]["embedding"])

            # Calculate pairwise similarities (cosine similarity)
            similarities = []
            if len(embeddings) > 1:
                from sklearn.metrics.pairwise import cosine_similarity
                import numpy as np

                vectors = np.array(all_vectors)
                sim_matrix = cosine_similarity(vectors)

                # Get average similarity (excluding diagonal)
                np.fill_diagonal(sim_matrix, 0)
                avg_similarity = sim_matrix.sum() / (
                    len(embeddings) * (len(embeddings) - 1)
                )

                similarities = sim_matrix.tolist()
            else:
                avg_similarity = 0.0
                similarities = []

        else:
            avg_vector = []
            vector_dimension = 0
            avg_similarity = 0.0
            similarities = []

        result = {
            "embeddings": embeddings,
            "model_used": model,
            "total_messages": len(messages),
            "vector_dimension": vector_dimension,
            "average_similarity": avg_similarity,
            "average_vector": avg_vector,
            "similarity_matrix": similarities,
            "usage": {
                "prompt_tokens": response.usage.prompt_tokens
                if hasattr(response, "usage")
                else 0,
                "total_tokens": response.usage.total_tokens
                if hasattr(response, "usage")
                else 0,
            },
            "provider": "OpenAI Embeddings API",
        }

        print(
            f"Embeddings generated using OpenAI {model} for {len(messages)} log messages"
        )
        return result

    except openai.OpenAIError as e:
        print(f"OpenAI API error: {e}")
        raise
    except Exception as e:
        print(f"Error generating embeddings: {e}")
        raise


def find_similar_logs(
    query: str, log_embeddings: List[Dict[str, Any]], top_k: int = 5
) -> List[Dict[str, Any]]:
    """Find similar logs using semantic search with embeddings."""
    if not log_embeddings or "embeddings" not in log_embeddings:
        return []

    # Embed the query
    query_result = embed_log_messages([query])

    if not query_result["embeddings"]:
        return []

    query_embedding = np.array(query_result["embeddings"][0]["embedding"])

    # Calculate similarities
    similarities = []
    for log_embedding in log_embeddings["embeddings"]:
        if "embedding" in log_embedding:
            log_vector = np.array(log_embedding["embedding"])

            # Calculate cosine similarity
            similarity = np.dot(query_embedding, log_vector) / (
                np.linalg.norm(query_embedding) * np.linalg.norm(log_vector)
            )

            similarities.append(
                {
                    "message": log_embedding.get("message", ""),
                    "similarity": float(similarity),
                    "index": log_embedding.get("index", 0),
                }
            )

    # Sort by similarity (descending)
    similarities.sort(key=lambda x: x["similarity"], reverse=True)

    # Return top-k results
    return similarities[:top_k]


def create_log_embedding_index(
    log_entries: List[Dict[str, Any]], field_to_embed: str = "message"
) -> Dict[str, Any]:
    """Create an embedding index for a collection of log entries."""
    messages = []
    entry_map = []

    for idx, entry in enumerate(log_entries):
        if field_to_embed in entry and isinstance(entry[field_to_embed], str):
            messages.append(entry[field_to_embed])
            entry_map.append({"entry_index": idx, "entry_data": entry})

    # Generate embeddings
    embedding_result = embed_log_messages(messages)

    # Map embeddings back to original entries
    for i, embedding_info in enumerate(embedding_result["embeddings"]):
        if i < len(entry_map):
            entry_map[i]["embedding"] = embedding_info["embedding"]
            entry_map[i]["embedding_index"] = embedding_info["index"]

    return {
        "embedding_model": embedding_result["model_used"],
        "total_entries": len(log_entries),
        "entries_with_embeddings": len(messages),
        "entry_map": entry_map,
        "embedding_stats": {
            "vector_dimension": embedding_result["vector_dimension"],
            "average_similarity": embedding_result["average_similarity"],
        },
    }
