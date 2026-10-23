from embeddings_client import get_embeddings_client
from embeddings_models import cosine_similarity

def calculate_similarity(text1: str, text2: str) -> float:
    """
    Calculates the cosine similarity between the embeddings of two texts.

    Args:
        text1: The first text string.
        text2: The second text string.

    Returns:
        The cosine similarity score between the two text embeddings.
    """
    client = get_embeddings_client()
    
    # Using a specific Cohere model for generating embeddings
    model = "embed-english-v3.0"
    
    # Generate embeddings for both texts in a single API call for efficiency
    response = client.embed(
        texts=[text1, text2],
        model=model,
        input_type="search_document"
    )
    
    embedding1 = response.embeddings[0]
    embedding2 = response.embeddings[1]
    
    # Calculate cosine similarity
    similarity = cosine_similarity(embedding1, embedding2)
    return similarity

