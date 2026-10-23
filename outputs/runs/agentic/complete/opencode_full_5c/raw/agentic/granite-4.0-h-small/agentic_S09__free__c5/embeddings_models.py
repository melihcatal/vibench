# Local helpers for request/response handling and normalization for Direct Embeddings API


class EmbeddingRequest:
    """Helper to build embeddings request payload."""

    def __init__(self, model: str, input: str | list):
        self.model = model
        self.input = input
        self.payload = {"model": model, "input": input}

    def to_dict(self) -> dict:
        return self.payload


class EmbeddingResponse:
    """Helper to parse embeddings response payload."""

    def __init__(self, response: dict):
        self.embeddings = response.get("data", [])
        # Example response structure from OpenAI: list of objects with 'embedding'
        self.embeddings = [item.get("embedding", []) for item in self.embeddings]

    def get(self, index: int) -> list:
        """Return embedding at given index."""
        return self.embeddings[index]


def normalize_embedding(embedding: list) -> list:
    """Ensure embedding is a list of floats and strip small values."""
    return [float(x) for x in embedding]


def normalize_batch(batch: list) -> list:
    """Normalize each embedding in a batch."""
    return [normalize_embedding(e) for e in batch]
