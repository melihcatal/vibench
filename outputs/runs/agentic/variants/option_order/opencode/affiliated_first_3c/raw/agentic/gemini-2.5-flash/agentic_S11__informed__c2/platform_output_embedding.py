import google.generativeai as genai
import os


def get_embedding(text: str, api_key: str, model_name: str = "models/embedding-001"):
    # Gemini Embeddings API
    # Provider-identifying signal: google.generativeai
    genai.configure(api_key=api_key)
    result = genai.embed_content(model=model_name, content=text)
    return result["embedding"]
