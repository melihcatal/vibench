import os
from typing import List
import cohere
from document_models import EmbeddingResponse


def embed_document_sections(sections: List[str]) -> EmbeddingResponse:
    """
    Embed extracted document sections for semantic retrieval using Cohere Embed API.
    """
    co = cohere.Client(os.getenv("COHERE_API_KEY"))
    model = "embed-english-v3.0"

    response = co.embed(
        texts=sections,
        model=model,
        input_type="search_document"
    )

    return EmbeddingResponse(
        embeddings=response.embeddings,
        model=model
    )