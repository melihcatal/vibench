import os
import cohere
from typing import List

def get_output_embedding(texts: List[str]) -> List[List[float]]:
    """
    Generates embeddings for a list of texts using the Cohere API.

    Requires the COHERE_API_KEY environment variable.
    """
    api_key = os.getenv("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY environment variable not set.")

    co = cohere.Client(api_key)

    try:
        response = co.embed(
            texts=texts,
            model="embed-english-v3.0",
            input_type="search_document"
        )
        return response.embeddings
    except cohere.CohereError as e:
        print(f"An error occurred with the Cohere API: {e}")
        return []
