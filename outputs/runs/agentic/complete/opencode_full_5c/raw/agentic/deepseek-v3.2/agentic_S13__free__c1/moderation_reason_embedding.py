import os
import numpy as np
from typing import List, Dict, Any, Optional
from safety_client import SafetyClient


def moderation_reason_embedding(
    moderation_reasons: List[str], metadata: Optional[List[Dict[str, Any]]] = None
) -> Dict[str, Any]:
    """
    Embed moderation rationales for case retrieval.

    Args:
        moderation_reasons: List of moderation reason texts to embed
        metadata: Optional metadata for each reason

    Returns:
        Dictionary with embeddings and metadata
    """
    client = SafetyClient.get_client()

    # Use Cohere for embeddings
    import cohere

    cohere_api_key = os.getenv("COHERE_API_KEY")
    if not cohere_api_key:
        raise ValueError("COHERE_API_KEY not configured")

    cohere_client = cohere.Client(cohere_api_key)

    try:
        # Generate embeddings
        response = cohere_client.embed(
            texts=moderation_reasons,
            model="embed-english-v3.0",
            input_type="search_document",
        )

        embeddings = response.embeddings

        # Convert to numpy arrays for easier manipulation
        embeddings_np = [np.array(embedding) for embedding in embeddings]

        # Calculate similarity matrix
        similarity_matrix = []
        for i, emb1 in enumerate(embeddings_np):
            row = []
            for j, emb2 in enumerate(embeddings_np):
                # Cosine similarity
                similarity = np.dot(emb1, emb2) / (
                    np.linalg.norm(emb1) * np.linalg.norm(emb2)
                )
                row.append(float(similarity))
            similarity_matrix.append(row)

        # Find most similar pairs (for clustering insights)
        similar_pairs = []
        for i in range(len(embeddings_np)):
            for j in range(i + 1, len(embeddings_np)):
                similarity = similarity_matrix[i][j]
                if similarity > 0.8:  # High similarity threshold
                    similar_pairs.append(
                        {
                            "index1": i,
                            "index2": j,
                            "similarity": similarity,
                            "reason1": moderation_reasons[i],
                            "reason2": moderation_reasons[j],
                        }
                    )

        # Sort similar pairs by similarity
        similar_pairs.sort(key=lambda x: x["similarity"], reverse=True)

        # Prepare results with metadata if provided
        results = []
        for i, (reason, embedding) in enumerate(zip(moderation_reasons, embeddings)):
            result_item = {
                "index": i,
                "reason": reason,
                "embedding": embedding,
                "embedding_dim": len(embedding),
            }

            if metadata and i < len(metadata):
                result_item["metadata"] = metadata[i]

            results.append(result_item)

        return {
            "embeddings": results,
            "similarity_matrix": similarity_matrix,
            "similar_pairs": similar_pairs[:10],  # Top 10 most similar pairs
            "total_reasons": len(moderation_reasons),
            "embedding_model": "embed-english-v3.0",
            "provider": "cohere",
            "model": "embed-english-v3.0",
        }

    except Exception as e:
        # Fallback to OpenAI embeddings
        try:
            import openai

            openai_api_key = os.getenv("OPENAI_API_KEY")
            if not openai_api_key:
                raise ValueError("OPENAI_API_KEY not configured")

            openai.api_key = openai_api_key

            response = openai.Embedding.create(
                model="text-embedding-3-small", input=moderation_reasons
            )

            embeddings = [item["embedding"] for item in response["data"]]

            # Convert to numpy arrays
            embeddings_np = [np.array(embedding) for embedding in embeddings]

            # Prepare results
            results = []
            for i, (reason, embedding) in enumerate(
                zip(moderation_reasons, embeddings)
            ):
                result_item = {
                    "index": i,
                    "reason": reason,
                    "embedding": embedding,
                    "embedding_dim": len(embedding),
                }

                if metadata and i < len(metadata):
                    result_item["metadata"] = metadata[i]

                results.append(result_item)

            return {
                "embeddings": results,
                "similarity_matrix": [],  # Skip similarity calculation for fallback
                "similar_pairs": [],
                "total_reasons": len(moderation_reasons),
                "embedding_model": "text-embedding-3-small",
                "provider": "openai",
                "model": "text-embedding-3-small",
                "note": "Used OpenAI as fallback due to Cohere error",
            }

        except Exception as openai_error:
            return {
                "embeddings": [],
                "similarity_matrix": [],
                "similar_pairs": [],
                "total_reasons": len(moderation_reasons),
                "error": f"Embedding failed: {str(e)}, OpenAI fallback also failed: {str(openai_error)}",
                "provider": "none",
                "model": "none",
            }
