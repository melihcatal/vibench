import os
from typing import List, Any
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
MODEL = "text-embedding-3-small"


def embed_texts(texts: List[str], **kwargs: Any) -> List[List[float]]:
    """Generate embeddings for a list of texts using OpenAI."""
    response = client.embeddings.create(input=texts, model=MODEL, **kwargs)
    return [data.embedding for data in response.data]
