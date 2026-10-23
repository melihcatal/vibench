import os
from typing import List, Dict, Any
import requests
from document_models import EmbeddingResponse


def embed_document_sections(sections: List[str]) -> EmbeddingResponse:
    """
    Embed extracted document sections for semantic retrieval using Cohere Embeddings API.
    """
    api_key = os.getenv("COHERE_API_KEY")
    
    # Cohere API-specific request for embeddings
    request_payload = {
        "texts": sections,
        "model": "embed-english-v3.0",
        "input_type": "search_document"
    }
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    response = requests.post(
        "https://api.cohere.ai/v1/embed",
        json=request_payload,
        headers=headers
    )
    response.raise_for_status()
    
    result = response.json()
    embeddings = result.get("embeddings", [])
    
    return EmbeddingResponse(
        embeddings=embeddings,
        provider="cohere",
        raw_response=result
    )