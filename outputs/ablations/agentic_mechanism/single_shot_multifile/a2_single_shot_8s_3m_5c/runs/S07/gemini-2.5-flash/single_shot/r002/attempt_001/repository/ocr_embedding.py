import os
import cohere

from document_client import get_cohere_client
from document_models import EmbeddingResponse

def embed_document_sections(texts: list[str]) -> EmbeddingResponse:
    client = get_cohere_client()

    response = client.embed(
        texts=texts,
        model="embed-english-v3.0",
        input_type="search_document"
    )

    return EmbeddingResponse(embeddings=response.embeddings)
