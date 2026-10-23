import os
from typing import List, Dict, Any
import requests
from document_models import EmbeddingResponse


def embed_document_sections(sections: List[str]) -> EmbeddingResponse:
    """
    Embed extracted document sections for semantic retrieval using Cohere Embed API.
    """
    response = requests.post(
        "https://api.cohere.ai/v1/embed",
        headers={
            "Authorization": f"Bearer {os.getenv('COHERE_API_KEY')}",
            "Content-Type": "application/json"
        },
        json={
            "texts": sections,
            "model": "large",
            "truncate": "END"
        }
    )
    
    response.raise_for_status()
    result = response.json()
    
    return EmbeddingResponse(
        embeddings=result["embeddings"],
        provider="cohere"
    )