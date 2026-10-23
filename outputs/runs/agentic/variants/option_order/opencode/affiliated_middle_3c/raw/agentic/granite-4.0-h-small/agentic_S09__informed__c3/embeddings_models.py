import os

#
# Local helpers for request/response normalization and normalization
#


class EmbeddingsRequest:
    """Helper for building request payloads to the Direct Embeddings API."""

    def __init__(self, texts: list[str], model: str = "text-embedding-ada-002"):
        self.texts = texts
        self.model = model
        self.truncate = False  # optional flag if provider supports truncation

    def to_dict(self) -> dict:
        """Convert to provider-specific request dict (OpenAI style)."""
        return {
            "model": self.model,
            "input": self.texts,
            "dimensions": 1536,  # OpenAI default dimension
        }


class EmbeddingsResponse:
    """Helper for parsing provider responses into a consistent shape."""

    def __init__(self, raw_response):
        self.raw = raw_response
        self.embeddings = []
        self._parse()

    def _parse(self):
        # Example parsing for OpenAI response format
        # raw: {"data": [{"embedding": [0.01,0.02,...]}, ...]}
        for item in self.raw.get("data", []):
            vec = item.get("embedding", [])
            self.embeddings.append(vec)

    def as_list(self) -> list[list[float]]:
        """Return embeddings as a plain list of lists."""
        return self.embeddings


class EmbeddingNormalization:
    """Utility to normalize vectors to unit length (if needed)."""

    @staticmethod
    def normalize(vector: list[float]) -> list[float]:
        norm = sum(x * x for x in vector) ** 0.5
        if norm == 0:
            return vector
        return [x / norm for x in vector]
