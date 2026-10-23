import os
import numpy as np
from typing import List, Dict, Any
from openai import OpenAI
from model_client import get_openai_client


def embed_platform_output(
    content: str, model: str = "text-embedding-3-small"
) -> Dict[str, Any]:
    """Embed platform outputs for evaluation or retrieval using OpenAI embeddings."""
    client = get_openai_client()

    # Generate embedding using OpenAI's embedding API
    response = client.embeddings.create(
        model=model,
        input=content,
        encoding_format="float",  # Get float array for numerical operations
    )

    embedding = response.data[0].embedding

    return {
        "embedding": embedding,
        "model": response.model,
        "usage": {
            "prompt_tokens": response.usage.prompt_tokens,
            "total_tokens": response.usage.total_tokens,
        },
        "embedding_length": len(embedding),
        "content_preview": content[:100] + "..." if len(content) > 100 else content,
    }


def embed_multiple_outputs(
    contents: List[str], model: str = "text-embedding-3-small"
) -> List[Dict[str, Any]]:
    """Embed multiple platform outputs in batch."""
    client = get_openai_client()

    # Batch embedding generation
    response = client.embeddings.create(
        model=model, input=contents, encoding_format="float"
    )

    results = []
    for i, data in enumerate(response.data):
        results.append(
            {
                "embedding": data.embedding,
                "index": i,
                "content_preview": contents[i][:100] + "..."
                if len(contents[i]) > 100
                else contents[i],
            }
        )

    return {
        "embeddings": results,
        "model": response.model,
        "usage": {
            "prompt_tokens": response.usage.prompt_tokens,
            "total_tokens": response.usage.total_tokens,
        },
        "batch_size": len(contents),
    }


def calculate_similarity(embedding1: List[float], embedding2: List[float]) -> float:
    """Calculate cosine similarity between two embeddings."""
    # Convert to numpy arrays
    vec1 = np.array(embedding1)
    vec2 = np.array(embedding2)

    # Calculate cosine similarity
    dot_product = np.dot(vec1, vec2)
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)

    if norm1 == 0 or norm2 == 0:
        return 0.0

    similarity = dot_product / (norm1 * norm2)
    return float(similarity)


def find_similar_outputs(
    query: str, stored_embeddings: List[Dict[str, Any]], top_k: int = 5
) -> List[Dict[str, Any]]:
    """Find similar outputs using embedding similarity."""
    # Embed the query
    query_embedding_result = embed_platform_output(query)
    query_embedding = query_embedding_result["embedding"]

    # Calculate similarities
    similarities = []
    for item in stored_embeddings:
        similarity = calculate_similarity(query_embedding, item["embedding"])
        similarities.append(
            {
                "content": item.get("content", ""),
                "similarity": similarity,
                "metadata": item.get("metadata", {}),
            }
        )

    # Sort by similarity (descending)
    similarities.sort(key=lambda x: x["similarity"], reverse=True)

    # Return top-k results
    return similarities[:top_k]


def get_available_embedding_models() -> List[Dict[str, Any]]:
    """Get available OpenAI embedding models."""
    return [
        {
            "id": "text-embedding-3-small",
            "dimensions": 1536,
            "max_tokens": 8191,
            "description": "Small, efficient embedding model",
        },
        {
            "id": "text-embedding-3-large",
            "dimensions": 3072,
            "max_tokens": 8191,
            "description": "Large, high-quality embedding model",
        },
        {
            "id": "text-embedding-ada-002",
            "dimensions": 1536,
            "max_tokens": 8191,
            "description": "Legacy embedding model",
        },
    ]


def create_embedding_store(
    contents: List[str], metadata: List[Dict[str, Any]] = None
) -> List[Dict[str, Any]]:
    """Create a store of embeddings with metadata."""
    if metadata is None:
        metadata = [{} for _ in range(len(contents))]

    # Embed all contents
    embedding_results = embed_multiple_outputs(contents)

    # Combine with metadata
    store = []
    for i, emb_result in enumerate(embedding_results["embeddings"]):
        store.append(
            {
                "embedding": emb_result["embedding"],
                "content": contents[i],
                "metadata": metadata[i],
                "index": i,
            }
        )

    return store


if __name__ == "__main__":
    # Example usage
    content1 = "Artificial intelligence is transforming industries."
    content2 = "Machine learning algorithms are becoming more sophisticated."
    content3 = "The weather today is sunny and warm."

    # Embed single output
    embedding1 = embed_platform_output(content1)
    print(f"Embedding 1 length: {embedding1['embedding_length']}")
    print(f"Model used: {embedding1['model']}")

    # Embed multiple outputs
    batch_result = embed_multiple_outputs([content1, content2, content3])
    print(f"\nBatch embeddings: {batch_result['batch_size']} items")

    # Calculate similarity
    emb1 = embedding1["embedding"]
    emb2 = embed_platform_output(content2)["embedding"]
    emb3 = embed_platform_output(content3)["embedding"]

    sim12 = calculate_similarity(emb1, emb2)
    sim13 = calculate_similarity(emb1, emb3)

    print(f"\nSimilarity between AI and ML content: {sim12:.4f}")
    print(f"Similarity between AI and weather content: {sim13:.4f}")

    # Create embedding store and search
    store = create_embedding_store(
        [content1, content2, content3],
        [{"topic": "AI"}, {"topic": "ML"}, {"topic": "weather"}],
    )

    similar = find_similar_outputs("deep learning neural networks", store, top_k=2)
    print(f"\nTop similar outputs for 'deep learning neural networks':")
    for item in similar:
        print(
            f"  Similarity: {item['similarity']:.4f}, Content: {item['content'][:50]}..."
        )
