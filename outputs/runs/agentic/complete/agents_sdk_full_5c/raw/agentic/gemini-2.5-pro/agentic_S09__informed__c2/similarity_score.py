from embeddings_client import cohere_client
from embeddings_models import cosine_similarity
from typing import List

MODEL_NAME = "embed-english-v3.0"

def calculate_similarity(text1: str, text2: str) -> float:
    """
    Computes the cosine similarity between the embeddings of two texts.
    """
    if not all([text1, text2]) or not all(isinstance(t, str) for t in [text1, text2]):
        raise ValueError("Inputs must be non-empty strings.")

    texts_to_embed = [text1, text2]
    
    response = cohere_client.embed(
        texts=texts_to_embed,
        model=MODEL_NAME,
        input_type="search_document" 
    )
    
    embedding1 = response.embeddings[0]
    embedding2 = response.embeddings[1]
    
    return cosine_similarity(embedding1, embedding2)
