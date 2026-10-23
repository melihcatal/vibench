import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()


class CaptionEmbedder:
    def __init__(self):
        GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
        if not GOOGLE_API_KEY:
            raise ValueError("GOOGLE_API_KEY environment variable not set.")
        genai.configure(api_key=GOOGLE_API_KEY)

    def embed_caption_chunk(self, text_chunk):
        if not text_chunk:
            return []

        response = genai.embed_content(
            model="models/embedding-001",
            content=text_chunk,
            task_type="RETRIEVAL_DOCUMENT",
        )
        return response["embedding"]
