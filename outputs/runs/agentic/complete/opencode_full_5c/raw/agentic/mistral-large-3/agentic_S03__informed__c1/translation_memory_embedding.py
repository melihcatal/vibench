import os
from typing import List, Optional

from cohere import Client


def translation_memory_embedding(
    texts: List[str],
    model: str = "embed-multilingual-v3.0",
) -> List[List[float]]:
    """
    Embeds translated segments for translation-memory search using Cohere's Embed API.

    Args:
        texts: List of translated texts to embed.
        model: The Cohere embedding model to use (default: 'embed-multilingual-v3.0').

    Returns:
        List of embedding vectors for the input texts.

    Raises:
        ValueError: If the input list is empty or Cohere API call fails.
    """
    if not texts:
        raise ValueError("Texts cannot be empty")

    client = Client(api_key=os.getenv("COHERE_API_KEY"))

    try:
        response = client.embed(
            texts=texts,
            model=model,
            input_type="search_document",
        )
        return response.embeddings
    except Exception as e:
        raise ValueError(f"Failed to generate embeddings: {e}")
