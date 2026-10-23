import os
import cohere
from typing import List


def embed_script(texts: List[str]) -> List[List[float]]:
    """
    Embeds narration scripts using Cohere Embed API.
    Requires COHERE_API_KEY environment variable to be set.
    """
    api_key = os.getenv("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY environment variable not set.")

    co = cohere.Client(api_key)

    try:
        response = co.embed(
            texts=texts,
            model="embed-english-v3.0",  # Or another suitable Cohere embedding model
            input_type="classification",  # Example input type, adjust as needed
        )
        return response.embeddings
    except cohere.CohereAPIError as e:
        raise RuntimeError(f"Cohere Embed API request failed: {e}")
