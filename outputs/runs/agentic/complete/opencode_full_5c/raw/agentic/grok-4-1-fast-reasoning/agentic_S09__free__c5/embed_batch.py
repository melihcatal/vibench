from typing import List
from embeddings_client import get_client
from embeddings_models import parse_embeddings


def embed_batch(texts: List[str]) -> List[List[float]]:
    client = get_client()
    response = client.embeddings.create(input=texts, model="text-embedding-3-small")
    return parse_embeddings(response)
