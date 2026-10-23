import os
from typing import Optional, Dict, Any
import google.generativeai as genai


class EmbeddingsClient:
    def __init__(
        self, api_key: Optional[str] = None, model: str = "models/embedding-001"
    ):
        """
        Initializes the Gemini Embeddings client with optional API key and model.
        """
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY environment variable not set.")
        genai.configure(api_key=self.api_key)
        self.model = model

    def get_client(self) -> Any:
        """
        Returns the configured Gemini client for embeddings.
        """
        return genai

    def get_model(self) -> str:
        """
        Returns the configured embedding model.
        """
        return self.model
