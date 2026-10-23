from typing import TypedDict


class EmbeddingRequest(TypedDict):
    input: str


class EmbeddingResponse(TypedDict):
    embedding: list[float]


def normalize_embedding(resp: EmbeddingResponse) -> list[float]:
    """Ensure embedding is a flat list of floats.

    Args:
        resp (EmbeddingResponse): Raw provider response.

    Returns:
        list[float]: Normalized embedding vector.
    """
    vec = resp.get("embedding")
    if not vec:
        raise ValueError("Response missing embedding field")
    return vec
