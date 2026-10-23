from typing import List, Dict, Any
import numpy as np


class EmbeddingResponse:
    """Normalize and parse embedding responses from Cohere Embed API."""

    def __init__(self, response: Dict[str, Any]):
        self.response = response
        self.embeddings = self._extract_embeddings()

    def _extract_embeddings(self) -> List[List[float]]:
        """Extract embeddings from the Cohere API response."""
        return [list(map(float, embedding)) for embedding in self.response.get("embeddings", [])]