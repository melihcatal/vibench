import os
import json
from typing import Literal

# Provider identified by SDK import and model identifier


class EmbeddingsModels:
    """Define local request, response, and normalization helpers for Direct Embeddings API."""

    SERVICE = "bedrock"  # Amazon Titan Embeddings via Bedrock Runtime
    MODEL_ID = "amazon.titan-text-premier-v1"
    CONTENT_TYPE = "text/plain"

    RequestShape = Dict[str, Any]
    ResponseShape = Dict[str, Any]

    @staticmethod
    def build_embed_text_payload(text: str) -> RequestShape:
        """Creates a request payload for single-text embedding."""
        return {
            "inputText": text,
            "contentType": EmbeddingsModels.CONTENT_TYPE,
            "modelId": EmbeddingsModels.MODEL_ID,
        }

    @staticmethod
    def build_embed_batch_payload(texts: List[str]) -> RequestShape:
        return {
            "inputTexts": texts,
            "contentType": EmbeddingsModels.CONTENT_TYPE,
            "modelId": EmbeddingsModels.MODEL_ID,
        }

    @staticmethod
    def extract_embedding(response: ResponseShape) -> List[float]:
        """Extracts the embedding vector from the raw response."""
        return response["embedding"]

    @staticmethod
    def extract_embeddings(response: ResponseShape) -> List[List[float]]:
        """Extracts a list of embedding vectors from batch response."""
        return response["embeddings"]

    @staticmethod
    def normalize_logits(logits: List[float]) -> List[float]:
        """Normalizes model logits to probabilities (optional helper)."""
        import numpy as np

        exps = np.exp(logits)
        return (exps / exps.sum()).tolist()

    @staticmethod
    def ensure_tensor(data: Any) -> List[float]:
        """Ensures numeric data is returned as float list."""
        if isinstance(data, (list, tuple)):
            return [float(v) for v in data]
        raise TypeError("Data must be list/tuple of numbers")

    @staticmethod
    def detect_provider(response: ResponseShape) -> Literal["bedrock"]:
        """Identifies the provider from the response shape."""
        return "bedrock"

    # Additional helpers can be added here as needed
