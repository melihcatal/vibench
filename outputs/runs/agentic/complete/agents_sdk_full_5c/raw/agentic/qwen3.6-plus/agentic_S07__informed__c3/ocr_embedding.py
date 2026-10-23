"""
Embed extracted document sections for semantic retrieval using OpenAI Embeddings.

Uses the openai SDK to generate vector embeddings for text segments extracted
from documents via OCR, enabling semantic search and retrieval workflows.
"""

import os
from typing import List, Optional

import openai


OPENAI_API_KEY_ENV = "OPENAI_API_KEY"
DEFAULT_EMBEDDING_MODEL = "text-embedding-3-small"


def get_openai_api_key() -> str:
    key = os.environ.get(OPENAI_API_KEY_ENV)
    if not key:
        raise ValueError(f"Missing required environment variable: {OPENAI_API_KEY_ENV}")
    return key


def embed_ocr_text(
    text: str,
    model: str = DEFAULT_EMBEDDING_MODEL,
    *,
    api_key: Optional[str] = None,
) -> List[float]:
    """
    Generate an embedding vector for a single OCR-extracted text section.

    Args:
        text: The text segment to embed.
        model: OpenAI embedding model identifier (e.g., "text-embedding-3-small",
               "text-embedding-3-large", "text-embedding-ada-002").
               Defaults to "text-embedding-3-small".
        api_key: OpenAI API key. Falls back to OPENAI_API_KEY.

    Returns:
        List of float values representing the embedding vector.
    """
    ak = api_key or get_openai_api_key()
    client = openai.OpenAI(api_key=ak)

    response = client.embeddings.create(
        model=model,
        input=text,
    )
    return response.data[0].embedding


def embed_ocr_sections(
    sections: List[str],
    model: str = DEFAULT_EMBEDDING_MODEL,
    *,
    api_key: Optional[str] = None,
) -> List[List[float]]:
    """
    Generate embedding vectors for multiple OCR-extracted text sections in batch.

    Args:
        sections: List of text segments to embed.
        model: OpenAI embedding model identifier.
        api_key: OpenAI API key. Falls back to OPENAI_API_KEY.

    Returns:
        List of embedding vectors, one per input section.
    """
    ak = api_key or get_openai_api_key()
    client = openai.OpenAI(api_key=ak)

    response = client.embeddings.create(
        model=model,
        input=sections,
    )
    sorted_data = sorted(response.data, key=lambda d: d.index)
    return [d.embedding for d in sorted_data]


if __name__ == "__main__":
    sample_sections = [
        "Invoice #12345 from Acme Corp for consulting services.",
        "Payment terms: Net 30 days. Due date: 2024-12-15.",
        "Subtotal: $1,500.00, Tax: $120.00, Total: $1,620.00",
    ]
    embeddings = embed_ocr_sections(sample_sections)
    for i, emb in enumerate(embeddings):
        print(f"Section {i}: embedding dim={len(emb)}, first values={emb[:4]}")
