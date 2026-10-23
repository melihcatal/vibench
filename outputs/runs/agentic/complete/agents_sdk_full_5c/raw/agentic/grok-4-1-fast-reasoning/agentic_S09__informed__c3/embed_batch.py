from typing import List
from embeddings_client import get_client, EMBEDDING_MODEL
from embeddings_models import extract_embeddings

def embed_batch(texts: list[str]) -> List[List[float]]:
    client = get_client()
    response = client.embeddings.create(
        input=texts,
        model=EMBEDDING_MODEL
    )
    return extract_embeddings(response)