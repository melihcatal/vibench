"""
Embed narration scripts for voice-asset search using OpenAI embeddings.

This module generates vector embeddings for narration scripts using
OpenAI's text-embedding-3-small and text-embedding-3-large models,
enabling semantic search across voice assets and script libraries.

Provider: OpenAI API (api.openai.com)
Model: text-embedding-3-small (default), text-embedding-3-large
"""

import os
from typing import Optional

from openai import OpenAI

# OpenAI configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
OPENAI_EMBEDDING_DIMENSIONS = 1536  # Default for text-embedding-3-small

# Available OpenAI embedding models
EMBEDDING_MODELS = {
    "text-embedding-3-small": {"dimensions": 1536, "max_tokens": 8191},
    "text-embedding-3-large": {"dimensions": 3072, "max_tokens": 8191},
    "text-embedding-ada-002": {"dimensions": 1536, "max_tokens": 8191},
}


def get_openai_client(api_key: Optional[str] = None) -> OpenAI:
    """
    Create an OpenAI client for embedding generation.
    
    Args:
        api_key: OpenAI API key
        
    Returns:
        Configured OpenAI client
    """
    key = api_key or OPENAI_API_KEY
    return OpenAI(api_key=key)


def embed_script(
    text: str,
    model: str = "text-embedding-3-small",
    dimensions: Optional[int] = None,
    client: Optional[OpenAI] = None,
) -> list[float]:
    """
    Generate embedding vector for a narration script using OpenAI.
    
    Args:
        text: Narration script text to embed
        model: OpenAI embedding model (text-embedding-3-small or text-embedding-3-large)
        dimensions: Optional output dimensions (for text-embedding-3 models)
        client: Optional pre-configured OpenAI client
        
    Returns:
        Embedding vector as list of floats
    """
    if not client:
        client = get_openai_client()
    
    kwargs = {
        "model": model,
        "input": text,
    }
    
    if dimensions and model in ("text-embedding-3-small", "text-embedding-3-large"):
        kwargs["dimensions"] = dimensions
    
    response = client.embeddings.create(**kwargs)
    
    return response.data[0].embedding


def embed_batch(
    scripts: list[str],
    model: str = "text-embedding-3-small",
    client: Optional[OpenAI] = None,
) -> list[list[float]]:
    """
    Generate embeddings for multiple narration scripts using OpenAI.
    
    Args:
        scripts: List of narration script texts
        model: OpenAI embedding model
        client: Optional pre-configured OpenAI client
        
    Returns:
        List of embedding vectors
    """
    if not client:
        client = get_openai_client()
    
    response = client.embeddings.create(
        model=model,
        input=scripts,
    )
    
    # Sort by index to maintain order
    sorted_data = sorted(response.data, key=lambda x: x.index)
    return [item.embedding for item in sorted_data]


def compute_similarity(
    embedding_a: list[float],
    embedding_b: list[float],
) -> float:
    """
    Compute cosine similarity between two OpenAI embedding vectors.
    
    Args:
        embedding_a: First embedding vector
        embedding_b: Second embedding vector
        
    Returns:
        Cosine similarity score (0 to 1)
    """
    if len(embedding_a) != len(embedding_b):
        raise ValueError("Embedding dimensions must match")
    
    dot_product = sum(a * b for a, b in zip(embedding_a, embedding_b))
    norm_a = sum(a * a for a in embedding_a) ** 0.5
    norm_b = sum(b * b for b in embedding_b) ** 0.5
    
    if norm_a == 0 or norm_b == 0:
        return 0.0
    
    return dot_product / (norm_a * norm_b)


def search_similar_scripts(
    query_text: str,
    script_embeddings: list[tuple[str, list[float]]],
    model: str = "text-embedding-3-small",
    top_k: int = 5,
    client: Optional[OpenAI] = None,
) -> list[tuple[str, float]]:
    """
    Search for similar narration scripts using OpenAI embeddings.
    
    Args:
        query_text: Query narration script
        script_embeddings: List of (script_text, embedding) tuples
        model: OpenAI embedding model for query
        top_k: Number of results to return
        client: Optional OpenAI client
        
    Returns:
        List of (script_text, similarity_score) tuples, sorted by similarity
    """
    # Embed the query using OpenAI text-embedding-3-small
    query_embedding = embed_script(query_text, model=model, client=client)
    
    # Compute similarities
    results = []
    for script_text, embedding in script_embeddings:
        similarity = compute_similarity(query_embedding, embedding)
        results.append((script_text, similarity))
    
    # Sort by similarity descending
    results.sort(key=lambda x: x[1], reverse=True)
    
    return results[:top_k]


def get_model_info(model: str = "text-embedding-3-small") -> dict:
    """
    Get information about an OpenAI embedding model.
    
    Args:
        model: Model name
        
    Returns:
        Dict with model dimensions and max tokens
    """
    return EMBEDDING_MODELS.get(model, {"dimensions": 1536, "max_tokens": 8191})


if __name__ == "__main__":
    scripts = [
        "Welcome to our product demonstration",
        "Thank you for choosing our services",
        "Please follow the instructions carefully",
    ]
    
    print("Generating embeddings with OpenAI text-embedding-3-small...")
    embeddings = embed_batch(scripts, model="text-embedding-3-small")
    print(f"Generated {len(embeddings)} embeddings, dimension: {len(embeddings[0])}")
    
    # Search example
    query = "Greetings for the demo"
    indexed = list(zip(scripts, embeddings))
    results = search_similar_scripts(query, indexed, top_k=2)
    print(f"\nQuery: '{query}'")
    for text, score in results:
        print(f"  [{score:.4f}] {text}")
