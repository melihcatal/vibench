import os
from model_client import get_gemini_client


def get_embedding(text: str) -> list[float]:
    genai = get_gemini_client()
    model = "embedding-001"
    response = genai.embed_content(model=model, content=text)
    return response["embedding"]
