from typing import List
from embeddings_client import EmbeddingsClient
from embeddings_models import cosine_similarity

def similarity_score(text1: str, text2: str) -> float:
    client = EmbeddingsClient()
    embs = client.embed_texts([text1, text2])
    return cosine_similarity(embs[0], embs[1])
