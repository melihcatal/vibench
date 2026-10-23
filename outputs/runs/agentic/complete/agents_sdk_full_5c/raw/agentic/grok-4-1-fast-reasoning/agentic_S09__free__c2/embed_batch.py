from typing import List
from embeddings_client import get_embeddings_client

EMBEDDING_MODEL = "text-embedding-3-small"

def embed_batch(texts: List[str]) -> List[List[float]]:
    client = get_embeddings_client()
    response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=texts
    )
    return [data.embedding for data in response.data]