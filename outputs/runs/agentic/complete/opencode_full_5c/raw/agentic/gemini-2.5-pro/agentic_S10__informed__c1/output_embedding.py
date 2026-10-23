import os
import cohere
from typing import List


def embed_output(text: str) -> List[float]:
    """
    Embed model outputs for clustering or retrieval using Cohere.
    """
    api_key = os.getenv("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY environment variable not set.")

    co = cohere.Client(api_key)

    try:
        response = co.embed(
            texts=[text], model="embed-english-v3.0", input_type="search_document"
        )
        if response.embeddings:
            return response.embeddings[0]
        return []
    except cohere.CohereError as e:
        print(f"Cohere API error: {e}")
        return []
