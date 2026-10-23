import numpy as np
from typing import List, Dict, Any
from embeddings_client import EmbeddingsClient
from embeddings_models import EmbeddingResponse, SimilarityScoreResponse

def _cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    dot_product = np.dot(vec1, vec2)
    norm_a = np.linalg.norm(vec1)
    norm_b = np.linalg.norm(vec2)
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot_product / (norm_a * norm_b)

def similarity_score(payload: Dict[str, Any], config: Dict[str, Any] = None) -> Dict[str, float]:
    config = config or {}
    client = EmbeddingsClient(api_key=config.get('api_key'))

    text1 = payload.get('text1')
    text2 = payload.get('text2')
    embedding1 = payload.get('embedding1')
    embedding2 = payload.get('embedding2')
    model = payload.get('model', 'text-embedding-3-small')

    if text1 and text2:
        emb_response1: EmbeddingResponse = client.embed(texts=[text1], model=model)
        emb_response2: EmbeddingResponse = client.embed(texts=[text2], model=model)
        vec1 = emb_response1.embedding
        vec2 = emb_response2.embedding
    elif embedding1 and embedding2:
        vec1 = embedding1
        vec2 = embedding2
    else:
        raise ValueError("Either 'text1' and 'text2' or 'embedding1' and 'embedding2' must be provided.")

    score = _cosine_similarity(vec1, vec2)
    return {'score': score}
