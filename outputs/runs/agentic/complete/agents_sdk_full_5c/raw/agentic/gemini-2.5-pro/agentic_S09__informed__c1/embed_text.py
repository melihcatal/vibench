from typing import List
from embeddings_client import get_cohere_client

# Note: Using a specific model version is a best practice.
COHERE_MODEL_NAME = "embed-english-v3.0"

def embed_text(text: str) -> List[float]:
    """
    Generates an embedding vector for a single text string using Cohere.

    Args:
        text: The text string to embed.

    Returns:
        The embedding vector for the text.
    """
    client = get_cohere_client()
    response = client.embed(
        texts=[text],
        model=COHERE_MODEL_NAME,
        input_type="search_document"
    )
    return response.embeddings[0]

