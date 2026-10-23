from typing import List
from embeddings_client import client
from embeddings_models import MODEL_ID, normalize_embedding

def embed_batch(texts: List[str]) -> List[List[float]]:
    if not texts:
        return []
    response = client.embeddings.create(
        model=MODEL_ID,
        input=texts
    )
    return [normalize_embedding(item.embedding) for item in response.data]