import os
import google.generativeai as genai
from typing import List, Dict, Any


class EmbeddingsClient:
    def __init__(self):
        genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
        self.model = "models/embedding-001"

    def embed_text(self, text: str) -> List[float]:
        """Generates an embedding for a single text string."""
        response = genai.embed_content(model=self.model, content=text)
        return response["embedding"]

    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """Generates embeddings for a batch of text strings."""
        response = genai.embed_content(model=self.model, content=texts)
        return response["embeddings"]
