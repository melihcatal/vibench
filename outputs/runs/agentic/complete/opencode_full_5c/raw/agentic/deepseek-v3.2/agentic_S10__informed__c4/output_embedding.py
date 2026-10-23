import os
import openai
from typing import List


def embed_text(text: str, model: str = "text-embedding-3-small") -> List[float]:
    """
    Embed model outputs for clustering or retrieval using OpenAI Embeddings.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")

    client = openai.OpenAI(api_key=api_key)

    response = client.embeddings.create(model=model, input=text)

    return response.data[0].embedding


def embed_texts(
    texts: List[str], model: str = "text-embedding-3-small"
) -> List[List[float]]:
    """
    Embed multiple texts using OpenAI Embeddings.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")

    client = openai.OpenAI(api_key=api_key)

    response = client.embeddings.create(model=model, input=texts)

    return [item.embedding for item in response.data]
