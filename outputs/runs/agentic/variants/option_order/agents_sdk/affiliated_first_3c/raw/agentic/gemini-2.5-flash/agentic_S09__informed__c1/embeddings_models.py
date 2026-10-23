from typing import List, Dict, Any

def normalize_embedding_response(response: Dict[str, Any]) -> List[List[float]]:
    """Normalizes an embedding API response to a list of embedding vectors.

    Args:
        response: The raw response dictionary from the embeddings API.

    Returns:
        A list of lists of floats, where each inner list is an embedding vector.
    """
    if "data" in response and isinstance(response["data"], list):
        return [item["embedding"] for item in response["data"] if "embedding" in item]
    return []

def prepare_text_for_embedding(text: str) -> str:
    """Prepares a single text string for embedding.
    (Currently a passthrough, but can include preprocessing if needed).
    """
    return text

def prepare_batch_for_embedding(texts: List[str]) -> List[str]:
    """Prepares a batch of text strings for embedding.
    (Currently a passthrough, but can include preprocessing if needed).
    """
    return texts
