import numpy as np
from typing import List
from embeddings_client import get_embedding
from embeddings_models import normalize_embedding, cosine_similarity

def similarity_score(text1: str, text2: str) -> float:
    emb1 = normalize_embedding(get_embedding(text1, model="text-embedding-3-small"))
    emb2 = normalize_embedding(get_embedding(text2, model="text-embedding-3-small"))
    return cosine_similarity(emb1, emb2)
