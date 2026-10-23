import os
from typing import Dict, Any, List
import requests
from document_models import EmbeddingResponse


def embed_document_sections(sections: List[str]) -> EmbeddingResponse:
    """
    Embed extracted document sections for semantic retrieval using Cohere Embeddings API.
    """
    api_key = os.getenv("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY environment variable not set")
    
    # Cohere Embeddings API-specific request
    request_payload = {
        "texts": sections,
        "model": "embed-english-v3.0",
        "input_type": "search_document"
    }
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
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