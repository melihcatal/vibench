"""
Embed extracted document sections for semantic retrieval using OpenAI Embeddings API.

Uses the OpenAI Embeddings API with text-embedding-3-small model to create
vector embeddings of OCR-extracted document sections for semantic search
and retrieval.
"""

import os
from typing import Optional, List, Dict, Any

import openai


# OpenAI Embeddings API configuration
OPENAI_API_HOST = "api.openai.com"
OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"
OPENAI_EMBEDDING_DIMENSION = 1536


def embed_ocr_text(
    text: str,
    model: str = OPENAI_EMBEDDING_MODEL,
    api_key: Optional[str] = None,
    dimensions: Optional[int] = OPENAI_EMBEDDING_DIMENSION,
) -> List[float]:
    """
    Generate embedding vector for a single OCR text segment.
    
    This function uses the OpenAI Embeddings API with the text-embedding-3-small
    model to create a vector embedding of the provided text for semantic
    search and retrieval.
    
    Args:
        text: The OCR-extracted text to embed.
        model: OpenAI embedding model to use.
        api_key: OpenAI API key (uses OPENAI_API_KEY env var if None).
        dimensions: Output embedding dimensions (optional, model-specific).
        
    Returns:
        List[float]: Embedding vector.
        
    Raises:
        ValueError: If text is empty.
        openai.APIError: If OpenAI API call fails.
    """
    if not text or not text.strip():
        raise ValueError("Text cannot be empty")
    
    client = openai.OpenAI(
        api_key=api_key or os.environ.get("OPENAI_API_KEY"),
    )
    
    kwargs = {
        "model": model,
        "input": text,
    }
    
    if dimensions and model in (OPENAI_EMBEDDING_MODEL, "text-embedding-3-large"):
        kwargs["dimensions"] = dimensions
    
    response = client.embeddings.create(**kwargs)
    
    return response.data[0].embedding


def embed_ocr_sections(
    sections: List[str],
    model: str = OPENAI_EMBEDDING_MODEL,
    api_key: Optional[str] = None,
    dimensions: Optional[int] = OPENAI_EMBEDDING_DIMENSION,
) -> List[List[float]]:
    """
    Generate embedding vectors for multiple OCR text sections.
    
    Args:
        sections: List of OCR-extracted text sections.
        model: OpenAI embedding model to use.
        api_key: OpenAI API key.
        dimensions: Output embedding dimensions.
        
    Returns:
        List[List[float]]: List of embedding vectors.
    """
    if not sections:
        return []
    
    non_empty_sections = [s for s in sections if s and s.strip()]
    if not non_empty_sections:
        return []
    
    client = openai.OpenAI(
        api_key=api_key or os.environ.get("OPENAI_API_KEY"),
    )
    
    kwargs = {
        "model": model,
        "input": non_empty_sections,
    }
    
    if dimensions and model in (OPENAI_EMBEDDING_MODEL, "text-embedding-3-large"):
        kwargs["dimensions"] = dimensions
    
    response = client.embeddings.create(**kwargs)
    
    return [item.embedding for item in response.data]


def embed_with_metadata(
    sections: List[Dict[str, Any]],
    model: str = OPENAI_EMBEDDING_MODEL,
    api_key: Optional[str] = None,
    dimensions: Optional[int] = OPENAI_EMBEDDING_DIMENSION,
) -> List[Dict[str, Any]]:
    """
    Generate embeddings for OCR sections with metadata.
    
    Each section dict should have a 'text' key and can have additional
    metadata keys that will be preserved in the output.
    
    Args:
        sections: List of dicts with 'text' key and optional metadata.
        model: OpenAI embedding model to use.
        api_key: OpenAI API key.
        dimensions: Output embedding dimensions.
        
    Returns:
        List[Dict[str, Any]]: List of dicts with embedding and metadata.
    """
    texts = [s.get("text", "") for s in sections if s.get("text", "").strip()]
    if not texts:
        return []
    
    embeddings = embed_ocr_sections(texts, model=model, api_key=api_key, dimensions=dimensions)
    
    result = []
    for i, section in enumerate(sections):
        if section.get("text", "").strip() and i < len(embeddings):
            result.append({
                "text": section["text"],
                "embedding": embeddings[i],
                "metadata": {k: v for k, v in section.items() if k != "text"},
            })
    
    return result


def cosine_similarity(vec_a: List[float], vec_b: List[float]) -> float:
    """
    Compute cosine similarity between two embedding vectors.
    
    Args:
        vec_a: First embedding vector.
        vec_b: Second embedding vector.
        
    Returns:
        float: Cosine similarity score (0.0 to 1.0).
    """
    if not vec_a or not vec_b:
        return 0.0
    
    dot_product = sum(a * b for a, b in zip(vec_a, vec_b))
    magnitude_a = sum(a * a for a in vec_a) ** 0.5
    magnitude_b = sum(b * b for b in vec_b) ** 0.5
    
    if magnitude_a == 0 or magnitude_b == 0:
        return 0.0
    
    return dot_product / (magnitude_a * magnitude_b)


def search_similar_sections(
    query: str,
    sections: List[str],
    top_k: int = 5,
    model: str = OPENAI_EMBEDDING_MODEL,
    api_key: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """
    Search for sections most similar to a query text.
    
    Args:
        query: Query text to search for.
        sections: List of OCR text sections to search.
        top_k: Number of top results to return.
        model: OpenAI embedding model to use.
        api_key: OpenAI API key.
        
    Returns:
        List[Dict[str, Any]]: Ranked list of similar sections with scores.
    """
    query_embedding = embed_ocr_text(query, model=model, api_key=api_key)
    section_embeddings = embed_ocr_sections(sections, model=model, api_key=api_key)
    
    scored_sections = []
    for i, section in enumerate(sections):
        if i < len(section_embeddings):
            score = cosine_similarity(query_embedding, section_embeddings[i])
            scored_sections.append({
                "text": section,
                "score": score,
                "index": i,
            })
    
    scored_sections.sort(key=lambda x: x["score"], reverse=True)
    return scored_sections[:top_k]
