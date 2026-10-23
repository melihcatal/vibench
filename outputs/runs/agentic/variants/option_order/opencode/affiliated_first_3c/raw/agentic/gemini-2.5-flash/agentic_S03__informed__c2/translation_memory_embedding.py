import google.generativeai as genai
import os


def embed_text_for_translation_memory(text: str) -> list[float]:
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = "models/embedding-001"  # Gemini Embeddings model
    response = genai.embed_content(model=model, content=text)
    return response["embedding"]
