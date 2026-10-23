import os
from typing import List, Dict, Any
import numpy as np
from openai import OpenAI
from model_client import get_openai_client


def platform_output_embedding(
    content: str, model: str = "text-embedding-3-small"
) -> Dict[str, Any]:
    """
    Embed platform outputs using OpenAI's embedding models for evaluation or retrieval.
    """
    client = get_openai_client()

    try:
        # Generate embedding using OpenAI's embedding API
        embedding_response = client.embeddings.create(
            model=model, input=content, encoding_format="float"
        )

        embedding_vector = embedding_response.data[0].embedding
        embedding_array = np.array(embedding_vector)

        # Calculate basic statistics
        embedding_stats = {
            "dimensions": len(embedding_vector),
            "norm": float(np.linalg.norm(embedding_array)),
            "mean": float(np.mean(embedding_array)),
            "std": float(np.std(embedding_array)),
            "min": float(np.min(embedding_array)),
            "max": float(np.max(embedding_array)),
        }

        embedding_metadata = {
            "provider": "openai",
            "embedding_model": model,
            "embedding_dimensions": embedding_response.data[0].embedding_dimensions,
            "usage": {
                "prompt_tokens": embedding_response.usage.prompt_tokens,
                "total_tokens": embedding_response.usage.total_tokens,
            },
            "object_type": embedding_response.object,
            "response_id": embedding_response.id,
        }

        return {
            "content": content,
            "embedding": embedding_vector,
            "embedding_stats": embedding_stats,
            "metadata": embedding_metadata,
            "raw_openai_response": embedding_response,
        }

    except Exception as e:
        raise Exception(
            f"Failed to generate embedding with OpenAI model {model}: {str(e)}"
        )


def compare_embeddings(
    embedding1: List[float], embedding2: List[float]
) -> Dict[str, Any]:
    """
    Compare two embeddings using cosine similarity and other metrics.
    """
    vec1 = np.array(embedding1)
    vec2 = np.array(embedding2)

    # Cosine similarity
    cosine_sim = np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

    # Euclidean distance
    euclidean_dist = np.linalg.norm(vec1 - vec2)

    # Dot product
    dot_product = np.dot(vec1, vec2)

    return {
        "cosine_similarity": float(cosine_sim),
        "euclidean_distance": float(euclidean_dist),
        "dot_product": float(dot_product),
        "vector_norm_1": float(np.linalg.norm(vec1)),
        "vector_norm_2": float(np.linalg.norm(vec2)),
    }
