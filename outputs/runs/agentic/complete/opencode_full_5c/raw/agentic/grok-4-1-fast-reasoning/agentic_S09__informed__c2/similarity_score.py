from typing import List
import math
from embeddings_client import get_embeddings_client, create_embedding
from embeddings_models import parse_embeddings_response

MODEL = "text-embedding-3-small"


def cosine_similarity(emb1: List[float], emb2: List[float]) -> float:
    dot = sum(a * b for a, b in zip(emb1, emb2))
    norm1 = math.sqrt(sum(a * a for a in emb1))
    norm2 = math.sqrt(sum(b * b for b in emb2))
    if norm1 == 0 or norm2 == 0:
        return 0.0
    return dot / (norm1 * norm2)


def similarity_score(text1: str, text2: str) -> float:
    client = get_embeddings_client()
    response = create_embedding(client, MODEL, [text1, text2])
    embs = parse_embeddings_response(response)
    return cosine_similarity(embs[0], embs[1])
