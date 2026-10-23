import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


def get_text_embedding(text: str) -> list[float]:
    model = "models/embedding-001"
    response = genai.embed_content(model=model, content=text)
    return response["embedding"]
