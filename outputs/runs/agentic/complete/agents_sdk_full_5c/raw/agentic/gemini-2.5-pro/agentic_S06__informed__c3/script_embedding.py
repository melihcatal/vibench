import os
import cohere
from typing import List

def embed_script(script_text: str) -> List[float]:
    """
    Embeds a narration script for search using Cohere.
    Expects COHERE_API_KEY environment variable.
    """
    api_key = os.environ.get("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY environment variable not set.")

    co = cohere.Client(api_key)

    try:
        response = co.embed(
            texts=[script_text],
            model="embed-english-v3.0",
            input_type="search_document"
        )
        return response.embeddings[0]
    except cohere.core.api_error.ApiError as e:
        print(f"An error occurred with the Cohere API: {e}")
        raise
