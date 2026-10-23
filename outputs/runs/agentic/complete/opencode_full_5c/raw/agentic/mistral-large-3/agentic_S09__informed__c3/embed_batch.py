import os
from openai import OpenAI
from typing import List

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def embed_batch(
    texts: List[str], model: str = "text-embedding-3-small"
) -> List[List[float]]:
    """Generate embeddings for a batch of texts using OpenAI Embeddings."""
    response = client.embeddings.create(input=texts, model=model)
    return [data.embedding for data in response.data]
