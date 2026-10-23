import google.generativeai as genai
from model_client import get_gemini_client
from model_models import GeminiModel


def get_embedding(text: str) -> list[float]:
    """Embeds model outputs for clustering or retrieval using Gemini Embeddings."""
    client = get_gemini_client()
    response = client.embed_content(model=GeminiModel.EMBEDDING, content=text)
    return response["embedding"]
