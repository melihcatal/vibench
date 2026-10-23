from typing import List
from embeddings_client import get_client
from embeddings_models import parse_embeddings, cosine_similarity


def similarity_score(text1: str, text2: str) -> float:
    client = get_client()
    response = client.embeddings.create(
        input=[text1, text2], model="text-embedding-3-small"
    )
    embeddings = parse_embeddings(response)
    return cosine_similarity(embeddings[0], embeddings[1])
