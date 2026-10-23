import os
from typing import List
import cohere

def embed_text(text: str) -> List[float]:
    """
    Embeds a single text string using the Cohere API.
    """
    api_key = os.environ.get("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY environment variable not set.")

    co = cohere.Client(api_key)
    
    response = co.embed(
        texts=[text],
        model="embed-english-v3.0",
        input_type="search_document"
    )
    
    # response.embeddings is a list of lists, we return the first one.
    return response.embeddings[0]
