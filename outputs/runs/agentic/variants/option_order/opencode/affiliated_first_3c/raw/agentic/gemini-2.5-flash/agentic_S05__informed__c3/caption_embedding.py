import google.generativeai as genai
import os

GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")


def embed_caption_chunk(chunk: str):
    if not GOOGLE_API_KEY:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")

    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel("embedding-001")

    result = model.embed_content(content=chunk, task_type="RETRIEVAL_DOCUMENT")
    return result["embedding"]
