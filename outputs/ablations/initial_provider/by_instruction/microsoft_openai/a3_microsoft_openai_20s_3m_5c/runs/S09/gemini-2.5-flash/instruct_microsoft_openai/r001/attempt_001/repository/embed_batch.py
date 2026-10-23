from typing import List
from embeddings_client import EmbeddingsClient
from embeddings_models import EmbeddingResponse

def embed_batch(texts: List[str], model: str = "text-embedding-ada-002") -> EmbeddingResponse:
    client = EmbeddingsClient()
    response = client.get_embeddings(texts=texts, model=model)
    return response
