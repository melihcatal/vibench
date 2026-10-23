from typing import List
from embeddings_client import get_client, EMBEDDING_MODEL
from embeddings_models import extract_embeddings, cosine_similarity

def similarity_score(text1: str, text2: str) -> float:
    client = get_client()
    response = client.embeddings.create(
        input=[text1, text2],
        model=EMBEDDING_MODEL
    )
    embeddings = extract_embeddings(response)
    return cosine_similarity(embeddings[0], embeddings[1])