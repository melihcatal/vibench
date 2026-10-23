import os
import cohere
from typing import List

def get_text_embedding(text: str) -> List[float]:
    """
    Generates an embedding for a given text using the Cohere API.

    Args:
        text: The input text to embed.

    Returns:
        A list of floats representing the embedding vector.
    """
    api_key = os.getenv("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY environment variable is not set.")

    # Provider-specific client: cohere.Client
    co = cohere.Client(api_key)

    # Provider-specific model identifier: "embed-english-v3.0"
    response = co.embed(
        texts=[text],
        model="embed-english-v3.0",
        input_type="search_document"
    )
    
    return response.embeddings[0]
