import os
from typing import List
import openai
from embeddings_client import get_embeddings_client


def embed_text(text: str, model: str = "text-embedding-3-small") -> List[float]:
    """Generate an embedding vector for one text string using OpenAI Embeddings."""
    client = get_embeddings_client()

    response = client.embeddings.create(
        model=model, input=text, encoding_format="float"
    )

    return response.data[0].embedding
