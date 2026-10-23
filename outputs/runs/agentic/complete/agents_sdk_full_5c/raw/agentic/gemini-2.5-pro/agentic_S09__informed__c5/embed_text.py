from typing import List
from embeddings_client import get_embeddings_client

def generate_text_embedding(text: str) -> List[float]:
    """
    Generates an embedding for a single text string using the Cohere API.

    Args:
        text: The text string to embed.

    Returns:
        A list of floats representing the embedding vector.
    """
    client = get_embeddings_client()
    
    # Using a specific Cohere model for embeddings
    model = "embed-english-v3.0"
    
    response = client.embed(
        texts=[text],
        model=model,
        input_type="search_document" 
    )
    
    # The response contains a list of embeddings, one for each input text.
    # Since we only provide one text, we take the first element.
    embedding = response.embeddings[0]
    return embedding

