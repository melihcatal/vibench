from embeddings_client import get_cohere_client
from embeddings_models import cosine_similarity

def calculate_embedding_similarity(text1: str, text2: str) -> float:
    """
    Computes the cosine similarity between the embeddings of two texts.

    Args:
        text1: The first text.
        text2: The second text.

    Returns:
        The cosine similarity score between the two text embeddings.
    """
    cohere_client = get_cohere_client()
    
    response = cohere_client.embed(
        texts=[text1, text2],
        model='embed-english-v3.0',
        input_type='search_document'
    )
    
    embedding1 = response.embeddings[0]
    embedding2 = response.embeddings[1]
    
    return cosine_similarity(embedding1, embedding2)

