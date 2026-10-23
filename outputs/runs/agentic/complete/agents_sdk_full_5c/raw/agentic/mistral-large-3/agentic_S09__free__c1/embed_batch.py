import os
from typing import List
from embeddings_client import get_embeddings_client
from embeddings_models import EmbeddingRequest, EmbeddingResponse

def embed_batch(texts: List[str]) -> List[List[float]]:
    client = get_embeddings_client()
    request = EmbeddingRequest(input=texts, model="text-embedding-3-small")
    response: EmbeddingResponse = client.embeddings.create(request.dict())
    return [item.embedding for item in sorted(response.data, key=lambda x: x.index)]