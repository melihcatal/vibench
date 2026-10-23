import os
from typing import List, Optional

import dashscope
from dashscope import TextEmbedding
from http import HTTPStatus


class DashScopeEmbeddingsClient:
    """
    Client for DashScope Text Embeddings API.
    Requires DASHSCOPE_API_KEY environment variable.
    """

    def __init__(self, model: str = "text-embedding-v2"):
        self.model = model
        self.api_key = os.getenv("DASHSCOPE_API_KEY")
        if not self.api_key:
            raise ValueError("DASHSCOPE_API_KEY environment variable not set")
        dashscope.api_key = self.api_key

    def embed(self, text: str) -> Optional[List[float]]:
        """Generate embedding for a single text string."""
        response = TextEmbedding.call(model=self.model, input=text)
        if response.status_code == HTTPStatus.OK:
            return response.output["embeddings"][0]["embedding"]
        else:
            raise Exception(f"DashScope API error: {response.message}")

    def batch_embed(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for a batch of texts."""
        response = TextEmbedding.call(model=self.model, input=texts)
        if response.status_code == HTTPStatus.OK:
            return [
                embedding["embedding"] for embedding in response.output["embeddings"]
            ]
        else:
            raise Exception(f"DashScope API error: {response.message}")
