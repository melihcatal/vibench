
import os
import cohere
from typing import List

def get_document_embeddings(texts: List[str]) -> List[List[float]]:
    """
    Generates embeddings for a list of document sections using Cohere.
    
    Reads API key from COHERE_API_KEY environment variable.
    """
    api_key = os.environ.get("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY environment variable is not set.")

    co = cohere.Client(api_key)

    response = co.embed(
        texts=texts,
        model="embed-english-v3.0",
        input_type="search_document"
    )
    
    return response.embeddings
