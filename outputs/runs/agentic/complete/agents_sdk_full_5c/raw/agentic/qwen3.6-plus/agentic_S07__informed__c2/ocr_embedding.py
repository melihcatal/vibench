"""
Embeds extracted document sections for semantic retrieval using the OpenAI Embeddings API.
Uses the official OpenAI Python SDK with the text-embedding-3-small model.
"""

import os
from typing import List, Dict, Any, Optional

from openai import OpenAI

from document_models import DocumentTextResult, DocumentLayoutResult, LayoutElement

# OpenAI Embedding model identifier
OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"


def get_openai_api_key() -> str:
    """Retrieve OpenAI API key from environment."""
    key = os.environ.get("OPENAI_API_KEY")
    if not key:
        raise ValueError("OPENAI_API_KEY environment variable is required")
    return key


def create_openai_client() -> OpenAI:
    """
    Create and return an authenticated OpenAI client.

    Returns:
        OpenAI: Authenticated OpenAI client for embeddings API.
    """
    api_key = get_openai_api_key()
    return OpenAI(api_key=api_key)


def embed_text(
    text: str,
    model: str = OPENAI_EMBEDDING_MODEL,
    dimensions: Optional[int] = None,
) -> List[float]:
    """
    Generate an embedding vector for a text string using OpenAI Embeddings API.

    Args:
        text: The text to embed.
        model: OpenAI embedding model identifier. Defaults to 'text-embedding-3-small'.
        dimensions: Optional number of dimensions for the embedding (model-dependent).

    Returns:
        List[float]: The embedding vector.
    """
    client = create_openai_client()
    params: Dict[str, Any] = {
        "model": model,
        "input": text,
    }
    if dimensions is not None:
        params["dimensions"] = dimensions

    response = client.embeddings.create(**params)
    return response.data[0].embedding


def embed_texts_batch(
    texts: List[str],
    model: str = OPENAI_EMBEDDING_MODEL,
    dimensions: Optional[int] = None,
) -> List[List[float]]:
    """
    Generate embedding vectors for a batch of text strings using OpenAI Embeddings API.

    Args:
        texts: List of text strings to embed.
        model: OpenAI embedding model identifier. Defaults to 'text-embedding-3-small'.
        dimensions: Optional number of dimensions for the embeddings.

    Returns:
        List[List[float]]: List of embedding vectors.
    """
    client = create_openai_client()
    params: Dict[str, Any] = {
        "model": model,
        "input": texts,
    }
    if dimensions is not None:
        params["dimensions"] = dimensions

    response = client.embeddings.create(**params)
    return [item.embedding for item in response.data]


def embed_ocr_blocks(
    ocr_result: DocumentTextResult,
    model: str = OPENAI_EMBEDDING_MODEL,
    dimensions: Optional[int] = None,
) -> List[Dict[str, Any]]:
    """
    Embed each text block from an OCR result using OpenAI Embeddings API.

    Creates embeddings for each block along with its metadata for semantic retrieval.

    Args:
        ocr_result: The DocumentTextResult from OCR extraction.
        model: OpenAI embedding model identifier. Defaults to 'text-embedding-3-small'.
        dimensions: Optional number of dimensions for the embeddings.

    Returns:
        List[Dict]: List of dicts with embedding, text, and metadata for each block.
    """
    non_empty_blocks = [
        block for block in ocr_result.blocks if block.content.strip()
    ]
    block_texts = [block.content for block in non_empty_blocks]

    if not block_texts:
        return []

    embeddings = embed_texts_batch(block_texts, model=model, dimensions=dimensions)

    results = []
    for block, embedding in zip(non_empty_blocks, embeddings):
        results.append({
            "text": block.content,
            "embedding": embedding,
            "confidence": block.confidence,
            "page_number": block.page_number,
            "bounding_box": block.bounding_box,
        })

    return results


def embed_layout_elements(
    layout_result: DocumentLayoutResult,
    model: str = OPENAI_EMBEDDING_MODEL,
    dimensions: Optional[int] = None,
    element_types: Optional[List[str]] = None,
) -> List[Dict[str, Any]]:
    """
    Embed layout elements from a document layout result using OpenAI Embeddings API.

    Args:
        layout_result: The DocumentLayoutResult from layout extraction.
        model: OpenAI embedding model identifier. Defaults to 'text-embedding-3-small'.
        dimensions: Optional number of dimensions for the embeddings.
        element_types: Optional filter for element types to embed.

    Returns:
        List[Dict]: List of dicts with embedding, text, and metadata for each element.
    """
    elements = layout_result.elements
    if element_types:
        elements = [e for e in elements if e.element_type in element_types]

    non_empty_elements = [e for e in elements if e.content.strip()]
    element_texts = [e.content for e in non_empty_elements]

    if not element_texts:
        return []

    embeddings = embed_texts_batch(element_texts, model=model, dimensions=dimensions)

    results = []
    for element, embedding in zip(non_empty_elements, embeddings):
        results.append({
            "text": element.content,
            "element_type": element.element_type,
            "embedding": embedding,
            "confidence": element.confidence,
            "page_number": element.page_number,
            "bounding_box": element.bounding_box,
        })

    return results


def embed_full_document(
    ocr_result: DocumentTextResult,
    model: str = OPENAI_EMBEDDING_MODEL,
    dimensions: Optional[int] = None,
) -> Dict[str, Any]:
    """
    Embed the full OCR document text and its blocks using OpenAI Embeddings API.

    Args:
        ocr_result: The DocumentTextResult from OCR extraction.
        model: OpenAI embedding model identifier. Defaults to 'text-embedding-3-small'.
        dimensions: Optional number of dimensions for the embedding.

    Returns:
        Dict: Dictionary with full document embedding and per-block embeddings.
    """
    full_embedding = embed_text(ocr_result.full_text, model=model, dimensions=dimensions)
    block_embeddings = embed_ocr_blocks(ocr_result, model=model, dimensions=dimensions)

    return {
        "full_text": ocr_result.full_text,
        "full_embedding": full_embedding,
        "block_embeddings": block_embeddings,
        "page_count": ocr_result.page_count,
        "model": model,
    }
