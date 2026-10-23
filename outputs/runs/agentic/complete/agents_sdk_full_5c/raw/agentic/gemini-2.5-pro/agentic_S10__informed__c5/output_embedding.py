import os
import cohere
from typing import List

def get_embedding(text: str, model: str = "embed-english-v3.0") -> List[float]:
    """
    Embed model outputs for clustering or retrieval using Cohere.
    """
    try:
        api_key = os.environ["COHERE_API_KEY"]
    except KeyError:
        raise ValueError("COHERE_API_KEY environment variable not set.")

    co = cohere.Client(api_key)

    response = co.embed(
        texts=[text],
        model=model,
        input_type="search_document"
    )
    
    return response.embeddings[0]

def get_embeddings(texts: List[str], model: str = "embed-english-v3.0") -> List[List[float]]:
    """
    Embed multiple model outputs using Cohere.
    """
    try:
        api_key = os.environ["COHERE_API_KEY"]
    except KeyError:
        raise ValueError("COHERE_API_KEY environment variable not set.")

    co = cohere.Client(api_key)

    response = co.embed(
        texts=texts,
        model=model,
        input_type="search_document"
    )
    
    return response.embeddings
