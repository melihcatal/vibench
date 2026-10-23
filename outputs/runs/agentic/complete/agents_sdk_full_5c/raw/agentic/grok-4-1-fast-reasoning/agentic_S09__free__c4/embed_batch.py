from embeddings_client import get_client
from embeddings_models import normalize_embedding
import numpy as np
from typing import List

EMBEDDING_MODEL = "text-embedding-3-small"

def embed_batch(texts: List[str]) -> List[List[float]]:
    client = get_client()
    response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=texts
    )
    embeddings = [np.array(data.embedding) for data in response.data]
    normalized_embeddings = [normalize_embedding(emb).tolist() for emb in embeddings]
    return normalized_embeddings