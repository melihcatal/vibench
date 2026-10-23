import os
from typing import List
from document_client import get_openai_client
from document_models import EmbeddingRequest, EmbeddingResponse


def ocr_embedding(
    text: str, model: str = "text-embedding-ada-002"
) -> EmbeddingResponse:
    """
    Embed extracted document sections for semantic retrieval using OpenAI Embeddings API.
    """
    openai = get_openai_client()

    response = openai.Embedding.create(model=model, input=text)

    embedding = response["data"][0]["embedding"]

    return EmbeddingResponse(
        embedding=embedding,
        model=model,
        provider="openai_embeddings",
        raw_response=response,
    )
