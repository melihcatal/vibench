import google.generativeai as genai
from model_client import get_gemini_client

def embed_text(text: str) -> list[float]:
    client = get_gemini_client()
    model = "models/text-embedding-004"
    result = client.embed_content(model=model, content=text)
    return result['embedding']
