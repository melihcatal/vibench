from typing import List
from embeddings_client import client
from embeddings_models import MODEL_ID, normalize_embedding

def similarity_score(text1: str, text2: str) -> float:
    resp1 = client.embeddings.create(model=MODEL_ID, input=[text1])
    emb1 = normalize_embedding(resp1.data[0].embedding)
    
    resp2 = client.embeddings.create(model=MODEL_ID, input=[text2])
    emb2 = normalize_embedding(resp2.data[0].embedding)
    
    dot_product = sum(e1 * e2 for e1, e2 in zip(emb1, emb2))
    return dot_product