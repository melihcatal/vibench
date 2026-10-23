import os
import google.generativeai as genai


def embed_caption_chunk(caption_chunk: str):
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable must be set.")
    genai.configure(api_key=api_key)

    model = genai.GenerativeModel("embedding-001")

    response = model.embed_content(model="models/embedding-001", content=caption_chunk)
    return response["embedding"]
