# embeddings_models.py - HELPER
# Local request/response and normalization helpers for Direct Embeddings API

from typing import List, Dict

# ------------------------------------------------------------------
# Request / Response Normalization for DashScope Embeddings
# ------------------------------------------------------------------


def normalize_embedding_response(resp: dict) -> List[List[float]]:
    """Convert DashScope response to a simple list of vectors.

    Args:
        resp (dict): Raw response from dashscope.embeddings.create.

    Returns:
        list of list of float: List where each element is an embedding vector.
    """
    return [item["data"] for item in resp.get("embeddings", [])]


# ------------------------------------------------------------------
# Helper to validate input texts before sending to the API
# ------------------------------------------------------------------


def validate_texts(texts: List[str]) -> None:
    """Check that texts list is not empty and each text is a non-empty string.

    Args:
        texts (list of str): Texts to validate.

    Raises:
        ValueError: If validation fails.
    """
    if not texts:
        raise ValueError("texts list cannot be empty")
    for idx, txt in enumerate(texts):
        if not isinstance(txt, str) or not txt.strip():
            raise ValueError(f"Text at index {idx} is empty or not a string")
