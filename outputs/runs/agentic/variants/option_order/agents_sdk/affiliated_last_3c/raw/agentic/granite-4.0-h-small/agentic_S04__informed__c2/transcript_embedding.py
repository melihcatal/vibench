import os
import requests
from openai import OpenAI

def transcript_embedding(segment: str, model="text-embedding-ada-002") -> dict:
    """Compute an embedding for a transcript segment using OpenAI's embedding API.
    Returns the embedding vector (list[float]) and metadata.
    """
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.embeddings.create(
        model=model,
        input=segment
    )
    # Response shape: {"data": [{"embedding": [...], "index": 0}]} for single input
    data = response.embeddings[0]
    return {
        "embedding": data.embedding,
        "index": data.index,
        "model": model,
    }
