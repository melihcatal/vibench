import os
import google.generativeai as genai

class GeminiEmbeddingsClient:
    """
    Provides a client for Google Gemini Embeddings API.
    Handles API key configuration.
    """
    def __init__(self):
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY environment variable not set.")
        genai.configure(api_key=api_key)
        self.model = "models/embedding-001"

    def get_embedding(self, text: str) -> list[float]:
        """Generates an embedding for a single text."""
        try:
            response = genai.get_embedding(
                model=self.model,
                content=text
            )
            return response['embedding']
        except Exception as e:
            print(f"Error getting embedding: {e}")
            return []

    def embed_batch(self, texts: list[str], task_type: str = "RETRIEVAL_DOCUMENT") -> list[list[float]]:
        """Generates embeddings for a batch of texts."""
        try:
            response = genai.embed_content(
                model=self.model,
                content=texts,
                task_type=task_type
            )
            return response['embeddings']
        except Exception as e:
            print(f"Error getting batch embeddings: {e}")
            return []

