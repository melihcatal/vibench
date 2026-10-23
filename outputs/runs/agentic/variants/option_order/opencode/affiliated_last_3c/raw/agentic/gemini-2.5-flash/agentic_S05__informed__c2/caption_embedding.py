import os
import google.generativeai as genai


def embed_caption_chunk(caption_chunk):
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

    response = genai.embed_content(model="models/embedding-001", content=caption_chunk)
    return response["embedding"]
