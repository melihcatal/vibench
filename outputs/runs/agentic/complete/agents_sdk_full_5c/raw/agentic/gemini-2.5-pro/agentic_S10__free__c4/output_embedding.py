import os
import cohere
from typing import List

def embed_text(text: str) -> List[float] | None:
    """
    Generates an embedding for a given text using Cohere.

    Args:
        text: The text to embed.

    Returns:
        A list of floats representing the embedding, or None on error.
    """
    api_key = os.getenv("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY environment variable not set.")

    try:
        co = cohere.Client(api_key)
        
        # Using a specific, identifiable Cohere model
        response = co.embed(
            texts=[text],
            model="embed-english-v3.0",
            input_type="search_document"
        )
        
        return response.embeddings[0]
        
    except cohere.errors.CohereError as e:
        print(f"An error occurred with the Cohere API: {e}")
        return None
