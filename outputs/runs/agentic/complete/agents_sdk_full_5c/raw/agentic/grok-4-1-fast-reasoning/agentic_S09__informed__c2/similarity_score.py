import numpy as np
from typing import List
from embeddings_client import get_client
from embeddings_models import create_request, normalize_embedding, cosine_similarity

def similarity_score(text1: str, text2: str) -> float:
    client = get_client()
    resp1 = client.embeddings.create(**create_request(text1))
    emb1 = normalize_embedding(resp1.data[0].embedding)
    resp2 = client.embeddings.create(**create_request(text2))
    emb2 = normalize_embedding(resp2.data[0].embedding)
    return cosine_similarity(emb1, emb2)
