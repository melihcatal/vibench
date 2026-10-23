"""
ocr_embedding.py - Embed extracted document sections for semantic retrieval
using OpenAI Embeddings API.

Provider: OpenAI
Model: text-embedding-3-small (OpenAI embedding model)
"""

from typing import Optional, Dict, Any, List

from openai import OpenAI
from openai import OpenAIError

from document_client import (
    DocumentClientConfig,
    get_openai_client,
)
from document_models import (
    OcrTextResult,
    LayoutResult,
)


def embed_ocr_text(
    ocr_result: OcrTextResult,
    client: Optional[OpenAI] = None,
    model: str = "text-embedding-3-small",
    dimensions: Optional[int] = None,
) -> Dict[str, Any]:
    """
    Generate embeddings for the full extracted OCR text using OpenAI.

    Args:
        ocr_result: OcrTextResult from OCR extraction.
        client: Optional pre-configured OpenAI client instance.
        model: OpenAI embedding model identifier.
        dimensions: Optional output dimensionality for the embedding.

    Returns:
        Dictionary with embedding vector, model info, and metadata.
    """
    if client is None:
        client = get_openai_client()

    text = ocr_result.extracted_text
    if not text or not text.strip():
        return {
            "embedding": [],
            "model": model,
            "text_length": 0,
            "dimensions": 0,
        }

    params: Dict[str, Any] = {
        "input": text,
        "model": model,
    }
    if dimensions is not None:
        params["dimensions"] = dimensions

    try:
        response = client.embeddings.create(**params)
    except OpenAIError as e:
        raise RuntimeError(f"OpenAI embedding generation failed with model {model}: {e}") from e

    embedding_data = response.data[0]
    vector = embedding_data.embedding
    usage = response.usage if hasattr(response, "usage") else None

    return {
        "embedding": vector,
        "model": model,
        "text_length": len(text),
        "dimensions": len(vector),
        "source_language": ocr_result.language,
        "source_ocr_confidence": ocr_result.confidence,
        "token_usage": usage.total_tokens if usage else 0,
    }


def embed_ocr_lines(
    ocr_result: OcrTextResult,
    client: Optional[OpenAI] = None,
    model: str = "text-embedding-3-small",
    dimensions: Optional[int] = None,
) -> List[Dict[str, Any]]:
    """
    Generate embeddings for each OCR line individually for
    granular semantic retrieval.

    Args:
        ocr_result: OcrTextResult from OCR extraction.
        client: Optional pre-configured OpenAI client instance.
        model: OpenAI embedding model identifier.
        dimensions: Optional output dimensionality.

    Returns:
        List of embedding results, one per line.
    """
    if client is None:
        client = get_openai_client()

    lines = ocr_result.lines if ocr_result.lines else []
    non_empty_lines = [line for line in lines if line.get("text", "").strip()]

    if not non_empty_lines:
        return []

    line_texts = [line.get("text", "") for line in non_empty_lines]

    params: Dict[str, Any] = {
        "input": line_texts,
        "model": model,
    }
    if dimensions is not None:
        params["dimensions"] = dimensions

    try:
        response = client.embeddings.create(**params)
    except OpenAIError as e:
        raise RuntimeError(f"OpenAI line embedding failed with model {model}: {e}") from e

    results = []
    for idx, embedding_obj in enumerate(response.data):
        line = non_empty_lines[idx]
        results.append({
            "line_index": idx,
            "text": line.get("text", ""),
            "embedding": embedding_obj.embedding,
            "model": model,
            "dimensions": len(embedding_obj.embedding),
            "bounding_box": line.get("bounding_box"),
            "words": line.get("words", []),
        })

    return results


def embed_layout_sections(
    layout_result: LayoutResult,
    client: Optional[OpenAI] = None,
    model: str = "text-embedding-3-small",
    dimensions: Optional[int] = None,
) -> List[Dict[str, Any]]:
    """
    Generate embeddings for layout sections (blocks) for semantic
    document retrieval.

    Args:
        layout_result: LayoutResult from layout extraction.
        client: Optional pre-configured OpenAI client instance.
        model: OpenAI embedding model identifier.
        dimensions: Optional output dimensionality.

    Returns:
        List of embedding results, one per meaningful block.
    """
    if client is None:
        client = get_openai_client()

    blocks = layout_result.blocks
    non_empty_blocks = [b for b in blocks if b.content and b.content.strip()]

    if not non_empty_blocks:
        return []

    block_texts = [block.content for block in non_empty_blocks]

    params: Dict[str, Any] = {
        "input": block_texts,
        "model": model,
    }
    if dimensions is not None:
        params["dimensions"] = dimensions

    try:
        response = client.embeddings.create(**params)
    except OpenAIError as e:
        raise RuntimeError(f"OpenAI layout embedding failed with model {model}: {e}") from e

    results = []
    for idx, embedding_obj in enumerate(response.data):
        block = non_empty_blocks[idx]
        results.append({
            "block_index": idx,
            "content": block.content,
            "kind": block.kind,
            "embedding": embedding_obj.embedding,
            "model": model,
            "dimensions": len(embedding_obj.embedding),
            "bounding_box": block.bounding_box,
            "spans": block.spans,
        })

    return results


def compute_embedding_similarity(
    embedding_a: List[float],
    embedding_b: List[float],
) -> float:
    """
    Compute cosine similarity between two embedding vectors.

    Args:
        embedding_a: First embedding vector.
        embedding_b: Second embedding vector.

    Returns:
        Cosine similarity score between 0 and 1.
    """
    import math

    if not embedding_a or not embedding_b:
        return 0.0

    dot_product = sum(a * b for a, b in zip(embedding_a, embedding_b))
    magnitude_a = math.sqrt(sum(a * a for a in embedding_a))
    magnitude_b = math.sqrt(sum(b * b for b in embedding_b))

    if magnitude_a == 0 or magnitude_b == 0:
        return 0.0

    return dot_product / (magnitude_a * magnitude_b)


def find_most_similar_section(
    query_embedding: List[float],
    section_embeddings: List[Dict[str, Any]],
    top_k: int = 3,
) -> List[Dict[str, Any]]:
    """
    Find the most similar document sections to a query embedding.

    Args:
        query_embedding: Query embedding vector.
        section_embeddings: List of section embedding dicts with 'embedding' key.
        top_k: Number of top results to return.

    Returns:
        List of section dicts with added similarity score, sorted descending.
    """
    scored_sections = []
    for section in section_embeddings:
        similarity = compute_embedding_similarity(query_embedding, section.get("embedding", []))
        scored = dict(section)
        scored["similarity"] = similarity
        scored_sections.append(scored)

    scored_sections.sort(key=lambda x: x["similarity"], reverse=True)
    return scored_sections[:top_k]
