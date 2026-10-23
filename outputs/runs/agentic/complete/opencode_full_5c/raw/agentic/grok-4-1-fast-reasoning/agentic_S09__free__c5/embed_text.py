from typing import List
from embeddings_client import get_client
from embeddings_models import parse_embeddings


def embed_text(text: str) -> List[float]:
    client = get_client()
    response = client.embeddings.create(input=text, model="text-embedding-3-small")
    return parse_embeddings(response)[0]
