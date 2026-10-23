from typing import List
from embeddings_client import get_embeddings_client
from embeddings_models import prepare_input, parse_embeddings


def embed_text(text: str) -> List[float]:
    client = get_embeddings_client()
    texts = prepare_input(text)
    response = client.embeddings.create(model="text-embedding-3-small", input=texts)
    embeddings = parse_embeddings(response)
    return embeddings[0]
