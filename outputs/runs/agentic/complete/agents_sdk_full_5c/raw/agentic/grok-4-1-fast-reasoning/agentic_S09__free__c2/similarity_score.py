from typing import List
from embeddings_client import get_embeddings_client
from embeddings_models import normalize_embedding, cosine_similarity

EMBEDDING_MODEL = "text-embedding-3-small"

def similarity_score(text1: str, text2: str) -> float:
    client = get_embeddings_client()
    resp1 = client.embeddings.create(model=EMBEDDING_MODEL, input=text1)
    resp2 = client.embeddings.create(model=EMBEDDING_MODEL, input=text2)
    emb1 = normalize_embedding(resp1.data[0].embedding)
    emb2 = normalize_embedding(resp2.data[0].embedding)
    return cosine_similarity(emb1, emb2)