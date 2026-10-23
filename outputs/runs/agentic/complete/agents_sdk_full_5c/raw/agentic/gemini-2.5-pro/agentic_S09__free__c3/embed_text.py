from embeddings_client import get_cohere_client

def generate_text_embedding(text: str):
    """
    Generates an embedding for a single text string.

    Args:
        text: The text to embed.

    Returns:
        A list of floats representing the embedding vector.
    """
    cohere_client = get_cohere_client()
    
    response = cohere_client.embed(
        texts=[text],
        model='embed-english-v3.0',
        input_type='search_document'
    )
    
    return response.embeddings[0]

