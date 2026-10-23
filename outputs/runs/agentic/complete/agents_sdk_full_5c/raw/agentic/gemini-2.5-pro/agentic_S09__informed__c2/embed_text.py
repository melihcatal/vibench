from embeddings_client import cohere_client
from typing import List

MODEL_NAME = "embed-english-v3.0"

def generate_embedding(text: str) -> List[float]:
    """
    Generates an embedding for a single text string.
    """
    if not text or not isinstance(text, str):
        raise ValueError("Input text must be a non-empty string.")

    response = cohere_client.embed(
        texts=[text],
        model=MODEL_NAME,
        input_type="search_document"
    )
    
    # The response contains a list of embeddings, one for each text.
    # We requested one, so we take the first.
    embedding = response.embeddings[0]
    return embedding
