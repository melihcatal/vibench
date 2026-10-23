import numpy as np
from typing import List, Dict, Any

EMBEDDING_MODEL_TEXT = "text-embedding-004"
EMBEDDING_MODEL_MULTILINGUAL = "text-embedding-preview-0409"


def normalize_embedding(embedding: List[float]) -> List[float]:
    """Normalizes an embedding vector."""
    norm = np.linalg.norm(embedding)
    if norm == 0:
        return embedding
    return (np.array(embedding) / norm).tolist()


def cosine_similarity(embedding1: List[float], embedding2: List[float]) -> float:
    """Computes the cosine similarity between two embedding vectors."""
    vec1 = np.array(embedding1)
    vec2 = np.array(embedding2)
    dot_product = np.dot(vec1, vec2)
    norm_vec1 = np.linalg.norm(vec1)
    norm_vec2 = np.linalg.norm(vec2)

    if norm_vec1 == 0 or norm_vec2 == 0:
        return 0.0
    return dot_product / (norm_vec1 * norm_vec2)


def format_embed_request(texts: List[str], model_id: str) -> Dict[str, Any]:
    """Formats a request for the Vertex AI embedding API."""
    instances = [{"content": text} for text in texts]
    return {"instances": instances, "parameters": {"model": model_id}}


def parse_embed_response(response: Any) -> List[List[float]]:
    """Parses the response from the Vertex AI embedding API."""
    embeddings = []
    for prediction in response.predictions:
        embeddings.append(prediction["embeddings"]["values"])
    return embeddings


def format_multilingual_embed_request(
    texts: List[str], model_id: str
) -> Dict[str, Any]:
    """Formats a request for the Vertex AI multilingual embedding API."""
    instances = [
        {"content": text, "task_type": "SEMANTIC_SIMILARITY"} for text in texts
    ]
    return {"instances": instances, "parameters": {"model": model_id}}
