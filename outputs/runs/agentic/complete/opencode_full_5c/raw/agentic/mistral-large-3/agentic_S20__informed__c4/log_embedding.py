import os
from openai import OpenAI
from typing import List, Dict


def log_embedding(texts: List[str]) -> List[List[float]]:
    """Embed selected log messages for semantic retrieval using OpenAI Embeddings."""
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    try:
        response = client.embeddings.create(model="text-embedding-ada-002", input=texts)
        return [embedding.embedding for embedding in response.data]
    except Exception as e:
        print(f"Failed to generate log embeddings using OpenAI: {e}")
        raise
