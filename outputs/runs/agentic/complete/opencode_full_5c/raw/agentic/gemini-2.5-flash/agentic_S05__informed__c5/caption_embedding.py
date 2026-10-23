import os
import google.generativeai as genai


def embed_caption_chunk(text_chunk: str) -> list:
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = "models/embedding-001"
    response = genai.embed_content(model=model, content=text_chunk)
    return response["embedding"]
