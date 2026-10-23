from typing import List, Dict, Any


def normalize_embedding(embedding: List[float]) -> List[float]:
    """L2-normalize an embedding vector.
    """
    import numpy as np
    vec = np.array(embedding, dtype=np.float32)
    norm = np.linalg.norm(vec)
    if norm == 0:
        return embedding  # avoid division by zero
    return list(vec / norm)


def batch_normalize_embeddings(embeddings: List[List[float]]) -> List[List[float]]:
    """Normalize a batch of embedding vectors in-place.
    """
    import numpy as np
    normalized = []
    for vec in embeddings:
        vec_arr = np.array(vec, dtype=np.float32)
        norm = np.linalg.norm(vec_arr)
        if norm == 0:
            normalized.append(vec)
        else:
            normalized.append(list(vec_arr / norm))
    return normalized


def parse_embedding_response(response: Dict[str, Any]) -> List[List[float]]:
    """Extract and normalize the embedding vectors from a provider response.
    Adjust the key names according to the actual provider's payload format.
    """
    # Example for OpenAI response format
    return [normalize_embedding(e['embedding']) for e in response.get('embeddings', [])]
