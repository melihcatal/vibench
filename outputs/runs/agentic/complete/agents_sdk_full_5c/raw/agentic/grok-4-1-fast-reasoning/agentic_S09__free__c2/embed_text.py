from typing import List
from embeddings_client import get_embeddings_client

EMBEDDING_MODEL = "text-embedding-3-small"

def embed_text(text: str) -> List[float]:
    client = get_embeddings_client()
    response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=text
    )
    return response.data[0].embedding