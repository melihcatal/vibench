import os
import cohere
from typing import List

def get_embedding(text: str) -> List[float]:
    """
    Generates an embedding for the given text using the Cohere API.

    Args:
        text: The text to embed.

    Returns:
        A list of floats representing the embedding.
    """
    api_key = os.getenv("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY environment variable not set.")

    co = cohere.Client(api_key)

    try:
        response = co.embed(
            texts=[text],
            model='embed-english-v3.0',
            input_type='search_document'
        )
        return response.embeddings[0]
    except cohere.CohereError as e:
        print(f"An error occurred with the Cohere API: {e}")
        return []

