from typing import List
from embeddings_client import get_embeddings_client
from embeddings_models import prepare_input, parse_embeddings


def embed_batch(texts: List[str]) -> List[List[float]]:
    client = get_embeddings_client()
    input_texts = prepare_input(texts)
    response = client.embeddings.create(
        model="text-embedding-3-small", input=input_texts
    )
    return parse_embeddings(response)
