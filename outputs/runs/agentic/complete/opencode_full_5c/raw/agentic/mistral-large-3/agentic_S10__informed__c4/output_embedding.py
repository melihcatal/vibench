import os
from typing import List, Dict, Any
from openai import OpenAI


def output_embedding(
    text: str, model_identifier: str = "text-embedding-3-small", api_key: str = None
) -> List[float]:
    """
    Embeds model outputs for clustering or retrieval using OpenAI Embeddings.

    Args:
        text: Text to embed.
        model_identifier: OpenAI embedding model identifier (e.g., "text-embedding-3-small").
        api_key: OpenAI API key. Defaults to OPENAI_API_KEY environment variable.

    Returns:
        Embedding vector as a list of floats.
    """
    api_key = api_key or os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set")

    client = OpenAI(api_key=api_key)

    response = client.embeddings.create(input=text, model=model_identifier)

    return response.data[0].embedding
