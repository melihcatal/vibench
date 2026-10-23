import os
from typing import List, Optional
from openai import OpenAI
from document_client import get_openai_client
from document_models import EmbeddingResult


def ocr_embedding(text: str, model: Optional[str] = None) -> EmbeddingResult:
    """
    Embed extracted document sections for semantic retrieval using OpenAI Embeddings API.

    Args:
        text: Text to embed
        model: Optional embedding model (default: text-embedding-3-small)

    Returns:
        EmbeddingResult containing text embedding vector
    """
    client = get_openai_client()

    model_id = model or "text-embedding-3-small"

    response = client.embeddings.create(
        model=model_id, input=text, encoding_format="float"
    )

    embedding = response.data[0].embedding

    return EmbeddingResult(
        text=text,
        embedding=embedding,
        provider="openai",
        model_id=model_id,
        dimensions=len(embedding),
        metadata={
            "prompt_tokens": response.usage.prompt_tokens,
            "total_tokens": response.usage.total_tokens,
        },
    )
