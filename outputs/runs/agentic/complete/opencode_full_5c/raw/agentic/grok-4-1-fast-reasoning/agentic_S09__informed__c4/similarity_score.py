from typing import List
from embeddings_client import get_embeddings_client
from embeddings_models import parse_embeddings, prepare_input


def cosine_similarity(emb1: List[float], emb2: List[float]) -> float:
    dot = sum(a * b for a, b in zip(emb1, emb2))
    norm1 = sum(a * a for a in emb1) ** 0.5
    norm2 = sum(b * b for b in emb2) ** 0.5
    return dot / (norm1 * norm2) if norm1 != 0 and norm2 != 0 else 0.0


def similarity_score(text1: str, text2: str) -> float:
    client = get_embeddings_client()
    texts = [text1, text2]
    response = client.embeddings.create(model="text-embedding-3-small", input=texts)
    embeddings = parse_embeddings(response)
    return cosine_similarity(embeddings[0], embeddings[1])
