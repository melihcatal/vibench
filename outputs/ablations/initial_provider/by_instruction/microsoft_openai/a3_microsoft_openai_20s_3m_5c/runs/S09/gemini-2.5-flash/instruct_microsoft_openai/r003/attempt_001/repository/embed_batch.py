import os
from openai import OpenAI
from typing import List
from embeddings_client import get_openai_client
from embeddings_models import EmbeddingVector

def embed_batch(texts: List[str]) -> List[EmbeddingVector]:
    client = get_openai_client()
    response = client.embeddings.create(
        input=texts,
        model="text-embedding-ada-002"
    )
    return [item.embedding for item in response.data]