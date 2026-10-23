import os
import cohere
from typing import List

def get_embedding_for_text(text: str) -> List[float] | None:
    """
    Generates an embedding for a given text string using the Cohere API.

    Args:
        text (str): The input text to embed.

    Returns:
        List[float] | None: The embedding vector, or None on failure.
    """
    api_key = os.environ.get("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY environment variable is not set.")

    try:
        co = cohere.Client(api_key)

        response = co.embed(
            texts=[text],
            model="embed-english-v3.0",
            input_type="search_document"
        )
        
        if response.embeddings:
            return response.embeddings[0]
        return None
    except Exception as e:
        print(f"An error occurred with the Cohere API: {e}")
        return None
