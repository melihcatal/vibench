import os
from typing import List
from embeddings_client import get_embeddings_client

def embed_text(text: str) -> List[float]:
    client = get_embeddings_client()
    response = client.embeddings.create(
        input=text,
        model="text-embedding-3-small"
    )
    return response.data[0].embedding