from typing import List
from model_client import client

def embed_outputs(texts: List[str]) -> List[List[float]]:
    """
    Generates embeddings for a list of text outputs using Cohere's embedding model.
    """
    response = client.embed(
        texts=texts,
        model="embed-english-v3.0",
        input_type="search_document"
    )
    
    return response.embeddings
