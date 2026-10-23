import os
from typing import List
from openai import OpenAI
from embeddings_client import get_client
from embeddings_models import create_request, normalize_embedding

def embed_text(text: str) -> List[float]:
    client = get_client()
    response = client.embeddings.create(**create_request(text))
    normalized_emb = normalize_embedding(response.data[0].embedding)
    return normalized_emb.tolist()
