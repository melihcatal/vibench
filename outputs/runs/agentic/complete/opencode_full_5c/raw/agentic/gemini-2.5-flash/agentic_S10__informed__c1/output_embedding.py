import os
import google.generativeai as genai
from model_client import get_gemini_client
from model_models import GeminiEmbeddingResponse


def embed_text(text: str) -> list[float]:
    """
    Embeds model outputs for clustering or retrieval using Google Gemini Embeddings.
    """
    client = get_gemini_client()
    result = client.embed_content(model="models/embedding-001", content=text)

    return GeminiEmbeddingResponse.from_gemini_embedding_response(result).embedding
