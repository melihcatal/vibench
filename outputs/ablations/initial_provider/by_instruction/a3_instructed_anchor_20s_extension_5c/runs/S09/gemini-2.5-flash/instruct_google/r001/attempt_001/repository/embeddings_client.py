import os
from typing import Any

import google.generativeai as genai

class EmbeddingsClient:
    """Provides client utilities for Google's Direct Embeddings API.
    """
    def __init__(self):
        api_key = os.environ.get("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY environment variable not set.")
        genai.configure(api_key=api_key)
        self._model = genai.get_model("embedding-001")

    def get_model(self) -> Any:
        """Returns the configured Google Generative AI embeddings model.

        Returns:
            The Generative AI model instance.
        """
        return self._model

