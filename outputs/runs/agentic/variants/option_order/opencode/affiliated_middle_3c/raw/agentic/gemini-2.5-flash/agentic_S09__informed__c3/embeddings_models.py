from typing import List, Dict, Any


def normalize_embedding_response(response: Any) -> List[float]:
    # Google Generative AI embedding response is typically a list of floats
    # If the structure is more complex, this function would adapt it.
    if hasattr(response, "embedding") and hasattr(response.embedding, "values"):
        return list(response.embedding.values)
    return []


def prepare_batch_request(texts: List[str]) -> List[Dict[str, Any]]:
    # For Google Generative AI, the model.embed_content method directly takes content.
    # This helper is more for standardization if different providers had varied batch input formats.
    return [{"content": text} for text in texts]
