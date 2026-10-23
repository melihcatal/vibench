# ocr_embedding.py
import os
from typing import List
import cohere

def get_text_embeddings(texts: List[str]) -> List[List[float]]:
    """
    Generates embeddings for a list of text strings using the Cohere API.

    Requires COHERE_API_KEY environment variable to be set.
    """
    api_key = os.getenv("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY must be set.")
        
    co = cohere.Client(api_key)

    response = co.embed(
        texts=texts,
        model="embed-english-v3.0",
        input_type="search_document"
    )
    
    return response.embeddings
