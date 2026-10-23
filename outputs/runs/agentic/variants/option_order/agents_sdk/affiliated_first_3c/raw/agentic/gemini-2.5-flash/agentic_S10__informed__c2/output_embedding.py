import os
import google.generativeai as genai
from model_client import get_gemini_embedding_client

def embed_text(text: str) -> list[float]:
    # The embedding model is specified in get_gemini_embedding_client
    # and the API key for Google Gemini is used.
    embedding_model = get_gemini_embedding_client()
    response = embedding_model.embed_content(model='embedding-001', content=text)
    return response['embedding']
