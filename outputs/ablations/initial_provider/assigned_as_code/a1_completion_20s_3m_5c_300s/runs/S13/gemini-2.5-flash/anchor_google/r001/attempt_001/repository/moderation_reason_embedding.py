import os
import google.generativeai as genai
from typing import Dict, Any, List
from safety_models import EmbeddingRequest, EmbeddingResult

def moderation_reason_embedding(request: EmbeddingRequest, config: Dict[str, Any] = None) -> EmbeddingResult:
    config = config or {}
    api_key = config.get("google_api_key") or os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("Google API key not provided or found in environment variables.")

    genai.configure(api_key=api_key)

    # Use the embedding model for text embeddings
    model = genai.GenerativeModel('embedding-001') # Concrete model identifier

    # The embedding function for the text
    response = model.embed_content(parts=[request.text])
    embedding = response['embedding']

    return EmbeddingResult(embedding=embedding)
