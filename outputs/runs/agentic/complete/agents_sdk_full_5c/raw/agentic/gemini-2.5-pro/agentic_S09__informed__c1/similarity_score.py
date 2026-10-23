from embeddings_client import get_cohere_client
from embeddings_models import cosine_similarity

# Note: Using a specific model version is a best practice.
COHERE_MODEL_NAME = "embed-english-v3.0"

def calculate_similarity(text1: str, text2: str) -> float:
    """
    Computes the cosine similarity between the embeddings of two texts.

    Args:
        text1: The first text string.
        text2: The second text string.

    Returns:
        The cosine similarity score between the two text embeddings.
    """
    client = get_cohere_client()
    response = client.embed(
        texts=[text1, text2],
        model=COHERE_MODEL_NAME,
        input_type="search_document"
    )
    
    embedding1 = response.embeddings[0]
    embedding2 = response.embeddings[1]
    
    similarity = cosine_similarity(embedding1, embedding2)
    return float(similarity)
