from typing import TypedDict

# Request model for embedding requests (common across providers)


class EmbeddingRequest(TypedDict):
    model: str  # Model identifier (e.g., 'text-embedding-3-large')
    input: str | list[str]  # Single text or list of texts


# Response model for embedding responses


class EmbeddingResponse(TypedDict):
    data: list[dict]  # List of embedding data objects


class EmbeddingData(TypedDict):
    embedding: list[float]  # Embedding vector as list of floats


# Normalization helpers (if needed) can be added here later
