import os
from typing import List
from openai import OpenAI


def embed_batch(
    texts: List[str], model: str = "text-embedding-3-small"
) -> List[List[float]]:
    """Generate embeddings for a batch of texts using OpenAI Embeddings."""
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    response = client.embeddings.create(
        model=model, input=texts, encoding_format="float"
    )

    return [item.embedding for item in response.data]
