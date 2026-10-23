import os
from typing import List
from embeddings_client import get_openai_embedding_client, OPENAI_EMBEDDING_MODEL

def embed_batch(texts: List[str]) -> List[List[float]]:
    client = get_openai_embedding_client()
    response = client.embeddings.create(
        input=texts,
        model=OPENAI_EMBEDDING_MODEL
    )
    return [item.embedding for item in response.data]
