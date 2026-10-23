from typing import List
from embeddings_client import EmbeddingsClient

def embed_text(text: str) -> List[float]:
    client = EmbeddingsClient()
    return client.embed_texts([text])[0]
