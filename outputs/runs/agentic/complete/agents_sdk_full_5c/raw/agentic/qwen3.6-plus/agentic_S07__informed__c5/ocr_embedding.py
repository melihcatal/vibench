"""
ocr_embedding.py - Embed extracted document sections for semantic retrieval
using OpenAI Embeddings API.

Provider: OpenAI Embeddings
SDK: openai
Auth: OPENAI_API_KEY
"""

import os
from openai import OpenAI


OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"


def get_openai_client():
    """Create and return an OpenAI client instance."""
    if not OPENAI_API_KEY:
        raise ValueError("Set OPENAI_API_KEY environment variable.")
    return OpenAI(api_key=OPENAI_API_KEY)


def embed_text(text: str, model: str = OPENAI_EMBEDDING_MODEL) -> list[float]:
    """
    Generate an embedding vector for a single text string using OpenAI Embeddings.

    Args:
        text: The text to embed.
        model: The embedding model to use (default: text-embedding-3-small).

    Returns:
        List of floats representing the embedding vector.
    """
    client = get_openai_client()
    response = client.embeddings.create(
        input=text,
        model=model,
    )
    return response.data[0].embedding


def embed_document_sections(
    sections: list[str],
    model: str = OPENAI_EMBEDDING_MODEL,
) -> list[list[float]]:
    """
    Generate embedding vectors for multiple document sections (e.g., paragraphs,
    pages, or extracted text blocks) using OpenAI Embeddings API.

    Args:
        sections: List of text strings to embed.
        model: The embedding model to use (default: text-embedding-3-small).

    Returns:
        List of embedding vectors, one per section.
    """
    client = get_openai_client()

    response = client.embeddings.create(
        input=sections,
        model=model,
    )

    embeddings = []
    for item in sorted(response.data, key=lambda x: x.index):
        embeddings.append(item.embedding)

    return embeddings


def embed_with_metadata(
    sections: list[dict],
    model: str = OPENAI_EMBEDDING_MODEL,
) -> list[dict]:
    """
    Generate embeddings for document sections with associated metadata.

    Args:
        sections: List of dicts with 'text' and optional 'metadata' keys.
        model: The embedding model to use.

    Returns:
        List of dicts with 'embedding', 'text', and 'metadata' keys.
    """
    texts = [section.get("text", "") for section in sections]
    embeddings = embed_document_sections(texts, model=model)

    results = []
    for i, section in enumerate(sections):
        results.append({
            "embedding": embeddings[i],
            "text": section.get("text", ""),
            "metadata": section.get("metadata", {}),
        })

    return results
