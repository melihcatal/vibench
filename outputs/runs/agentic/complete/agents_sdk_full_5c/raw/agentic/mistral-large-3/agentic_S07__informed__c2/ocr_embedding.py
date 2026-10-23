from typing import List, Optional
import os
import cohere
from document_models import EmbeddingResponse


def embed_document_sections(sections: List[str], model: str = "embed-english-v3.0") -> EmbeddingResponse:
    """Embed extracted document sections for semantic retrieval using Cohere Embeddings."""
    api_key = os.getenv("COHERE_API_KEY")
    
    if not api_key:
        raise ValueError("COHERE_API_KEY must be set in environment variables.")
    
    co = cohere.Client(api_key)
    response = co.embed(texts=sections, model=model, input_type="search_document")
    
    return EmbeddingResponse(embeddings=response.embeddings, model=model)