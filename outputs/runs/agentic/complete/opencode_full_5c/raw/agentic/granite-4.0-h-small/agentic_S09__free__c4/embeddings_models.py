from typing import TypedDict, List


class EmbeddingRequest(TypedDict):
    """Payload for a single embedding request."""

    input: str


class EmbeddingResponse(TypedDict):
    """Response from a single embedding request."""

    embedding: List[float]
    model: str


class EmbeddingBatchRequest(TypedDict):
    """Payload for batch embedding requests."""

    inputs: List[str]


class EmbeddingBatchResponse(TypedDict):
    embeddings: List[EmbeddingResponse]


def normalize_embedding_response(resp: EmbeddingResponse) -> dict:
    """Extract useful fields and convert to a plain dict."""
    return {"embedding": resp["embedding"], "model": resp["model"]}


def normalize_embedding_batch_response(resp: EmbeddingBatchResponse) -> List[dict]:
    """Normalize a batch response into a list of dicts."""
    return [normalize_embedding_response(r) for r in resp["embeddings"]]
