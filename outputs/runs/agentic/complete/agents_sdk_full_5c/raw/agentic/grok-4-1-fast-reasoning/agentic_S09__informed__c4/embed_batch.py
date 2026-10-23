import os
from openai import OpenAI
from embeddings_client import EMBEDDING_MODEL
from typing import List

def embed_batch(texts: List[str]) -> List[List[float]]:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.embeddings.create(
        input=texts,
        model=EMBEDDING_MODEL
    )
    return [data.embedding for data in response.data]