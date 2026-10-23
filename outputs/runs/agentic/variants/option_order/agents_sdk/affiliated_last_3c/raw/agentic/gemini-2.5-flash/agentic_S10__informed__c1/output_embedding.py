import google.generativeai as genai
import os
from typing import List
from model_client import get_gemini_embedding_model
from model_models import EmbeddingRequest, EmbeddingResponse

def embed_text(texts: List[str], model_name: str = "models/embedding-001") -> EmbeddingResponse:
    """
    Embeds model outputs for clustering or retrieval using Gemini Embeddings.
    """
    embedding_model = get_gemini_embedding_model(model_name)
    request = EmbeddingRequest(
        model_name=model_name,
        text=texts
    )
    result = embedding_model.embed_content(content=request.text)
    embeddings = [embedding.values for embedding in result['embedding']]
    return EmbeddingResponse(embeddings=embeddings)
