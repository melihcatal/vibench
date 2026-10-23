from typing import List
from embeddings_client import get_embedding

def embed_text(text: str) -> List[float]:
    return get_embedding(text, model="text-embedding-3-small")
