import os
from openai import OpenAI
from document_client import get_openai_client
from document_models import EmbeddingRequest, EmbeddingResponse


def ocr_embedding(request: EmbeddingRequest) -> EmbeddingResponse:
    """Embed extracted document sections for semantic retrieval using OpenAI Embeddings API."""
    client = get_openai_client()

    model = request.model or "text-embedding-3-small"

    response = client.embeddings.create(
        model=model, input=request.text, encoding_format="float"
    )

    embedding = response.data[0].embedding

    return EmbeddingResponse(
        embedding=embedding, provider="openai", model_id=model, raw_response=response
    )
