import os
from typing import List

from document_client import get_cohere_client
from document_models import EmbeddingInput, EmbeddingOutput

def embed_ocr_sections(
    embedding_input: EmbeddingInput,
    model_name: str = "embed-english-v3.0", # Or other Cohere embedding model
    input_type: str = "search_document", # 'search_document', 'search_query', 'classification', 'clustering'
) -> EmbeddingOutput:
    """Embeds extracted document sections for semantic retrieval using Cohere Embeddings API."""
    client = get_cohere_client()

    response = client.embed(
        texts=embedding_input.text_segments,
        model=model_name,
        input_type=input_type,
    )

    embeddings: List[List[float]] = response.embeddings

    return EmbeddingOutput(embeddings=embeddings)
