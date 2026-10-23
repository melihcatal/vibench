import os
from typing import List
import google.generativeai as genai

GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")


class GeminiReasonEmbedder:
    def __init__(self):
        if not GOOGLE_API_KEY:
            raise ValueError("GOOGLE_API_KEY environment variable not set.")
        genai.configure(api_key=GOOGLE_API_KEY)

    def embed_rationale(self, rationales: List[str]) -> List[List[float]]:
        """Embed moderation rationales for case retrieval using Gemini Embeddings."""
        result = genai.embed_content(
            model="models/embedding-001",
            content=rationales,
            task_type="RETRIEVAL_DOCUMENT",
        )
        return [embedding.tolist() for embedding in result["embedding"]]
