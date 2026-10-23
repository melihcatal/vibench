import os
from typing import List, Dict, Any
import numpy as np
from openai import OpenAI


def platform_output_embedding(
    texts: List[str], model: str = "text-embedding-3-small"
) -> Dict[str, Any]:
    """
    Embed platform outputs for evaluation or retrieval using OpenAI's embedding API.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")

    client = OpenAI(api_key=api_key)

    # Generate embeddings for each text
    embeddings = []
    embedding_details = []

    for text in texts:
        response = client.embeddings.create(
            model=model, input=text, encoding_format="float"
        )

        embedding = response.data[0].embedding
        embeddings.append(embedding)

        embedding_details.append(
            {
                "text": text,
                "embedding_vector": embedding,
                "embedding_model": response.model,
                "embedding_object": response.object,
                "usage": {
                    "prompt_tokens": response.usage.prompt_tokens,
                    "total_tokens": response.usage.total_tokens,
                },
            }
        )

    # Convert to numpy arrays for easier computation
    embedding_array = np.array(embeddings)

    # Calculate similarity matrix if we have multiple texts
    similarity_matrix = None
    if len(texts) > 1:
        # Normalize embeddings
        norms = np.linalg.norm(embedding_array, axis=1, keepdims=True)
        normalized_embeddings = embedding_array / norms

        # Compute cosine similarity matrix
        similarity_matrix = np.dot(normalized_embeddings, normalized_embeddings.T)

    # Calculate average embedding
    average_embedding = np.mean(embedding_array, axis=0).tolist()

    # Calculate embedding statistics
    embedding_stats = {
        "num_texts": len(texts),
        "embedding_dimension": len(embeddings[0]) if embeddings else 0,
        "average_embedding_magnitude": float(np.linalg.norm(average_embedding)),
        "embedding_variance": float(np.var(embedding_array)) if len(texts) > 1 else 0.0,
    }

    result = {
        "embeddings": embedding_details,
        "embedding_array": embedding_array.tolist(),
        "average_embedding": average_embedding,
        "similarity_matrix": similarity_matrix.tolist()
        if similarity_matrix is not None
        else None,
        "embedding_stats": embedding_stats,
        "embedding_model": model,
    }

    return result
