from embeddings_client import get_client
from embeddings_models import cosine_similarity
import numpy as np
from typing import List

EMBEDDING_MODEL = "text-embedding-3-small"

def similarity_score(text1: str, text2: str) -> float:
    client = get_client()
    response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=[text1, text2]
    )
    emb1 = np.array(response.data[0].embedding)
    emb2 = np.array(response.data[1].embedding)
    return cosine_similarity(emb1, emb2)