import os
from typing import List
from embeddings_client import get_embeddings_client
from embeddings_models import EmbeddingRequest, EmbeddingResponse

def embed_text(text: str) -> List[float]:
    client = get_embeddings_client()
    request = EmbeddingRequest(input=text, model="text-embedding-3-small")
    response: EmbeddingResponse = client.embeddings.create(request.dict())
    return response.data[0].embedding