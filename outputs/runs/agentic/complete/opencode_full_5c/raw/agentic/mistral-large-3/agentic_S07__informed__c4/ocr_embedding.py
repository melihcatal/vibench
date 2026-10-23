from openai import OpenAI
import os
from typing import List
from document_client import get_document_client, load_config
from document_models import EmbeddingResponse


def embed_document_sections(sections: List[str]) -> EmbeddingResponse:
    """
    Embeds extracted document sections for semantic retrieval using OpenAI Embeddings.

    Args:
        sections: List of document sections or text chunks to embed.

    Returns:
        EmbeddingResponse containing embeddings and metadata.
    """
    client = get_document_client("openai")
    config = load_config("openai")

    api_key = config.get("api_key")

    if not api_key:
        raise ValueError("OpenAI API key must be set in environment variables.")

    response = client.embeddings.create(input=sections, model="text-embedding-ada-002")

    embeddings = [data.embedding for data in response.data]

    return EmbeddingResponse(
        embeddings=embeddings, provider="openai", model="text-embedding-ada-002"
    )
