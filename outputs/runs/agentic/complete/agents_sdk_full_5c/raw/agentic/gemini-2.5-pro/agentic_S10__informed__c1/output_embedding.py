import os
import cohere
from typing import List

def get_embedding(text: str) -> List[float]:
    """
    Generates an embedding for the given text using the Cohere API.
    """
    api_key = os.getenv("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY environment variable is not set.")

    co = cohere.Client(api_key)

    try:
        response = co.embed(
            texts=[text],
            model="embed-english-v3.0",
            input_type="search_document"
        )
        if response.embeddings:
            return response.embeddings[0]
        return []
    except cohere.CohereError as e:
        print(f"Cohere API error: {e}")
        return []

