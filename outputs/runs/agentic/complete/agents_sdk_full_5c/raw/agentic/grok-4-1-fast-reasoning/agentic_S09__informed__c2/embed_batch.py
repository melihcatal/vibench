import os
from typing import List
from openai import OpenAI
from embeddings_client import get_client
from embeddings_models import create_request, normalize_embedding

def embed_batch(texts: List[str]) -> List[List[float]]:
    client = get_client()
    response = client.embeddings.create(**create_request(texts))
    normalized_embs = [normalize_embedding(data.embedding).tolist() for data in response.data]
    return normalized_embs
