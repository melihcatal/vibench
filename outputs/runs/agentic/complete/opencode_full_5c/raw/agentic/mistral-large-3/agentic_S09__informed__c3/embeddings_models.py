from typing import List, Dict, Any, Optional
import numpy as np


class EmbeddingRequest:
    """Helper for embedding request normalization."""

    @staticmethod
    def normalize_text(text: str) -> str:
        """Normalize text for embedding."""
        return text.strip()

    @staticmethod
    def normalize_texts(texts: List[str]) -> List[str]:
        """Normalize a list of texts for embedding."""
        return [EmbeddingRequest.normalize_text(text) for text in texts]


class EmbeddingResponse:
    """Helper for embedding response parsing."""

    @staticmethod
    def validate_embedding(embedding: List[float]) -> bool:
        """Validate an embedding vector."""
        return len(embedding) > 0 and all(
            isinstance(x, (float, int)) for x in embedding
        )

    @staticmethod
    def validate_embeddings(embeddings: List[List[float]]) -> bool:
        """Validate a list of embedding vectors."""
        return all(
            EmbeddingResponse.validate_embedding(embedding) for embedding in embeddings
        )
