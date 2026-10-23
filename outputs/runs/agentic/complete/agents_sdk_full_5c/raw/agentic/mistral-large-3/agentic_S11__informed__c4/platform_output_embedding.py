import cohere
import os
from typing import List, Dict, Any


def embed_output(text: str) -> Dict[str, Any]:
    """Generate embeddings for text using Cohere Embed API."""
    co = cohere.Client(os.getenv("COHERE_API_KEY"))
    
    response = co.embed(
        texts=[text],
        model="embed-english-v3.0",
        input_type="search_document"
    )
    
    return {
        "embeddings": response.embeddings,
        "text": text,
        "model": "embed-english-v3.0"
    }