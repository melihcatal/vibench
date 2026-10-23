from embeddings_client import get_vertex_client
from embeddings_models import cosine_similarity, GOOGLE_EMBEDDING_MODEL

def calculate_similarity(text1: str, text2: str) -> float:
    """
    Embeds two texts and computes their cosine similarity using Google Vertex AI.

    Args:
        text1: The first text string.
        text2: The second text string.

    Returns:
        The cosine similarity score between the two text embeddings.
    """
    if not all(isinstance(t, str) and t for t in [text1, text2]):
        raise ValueError("Input texts must be non-empty strings.")

    client = get_vertex_client()
    embeddings = client.get_embeddings([text1, text2], model_name=GOOGLE_EMBEDDING_MODEL)
    
    vector1 = embeddings[0].values
    vector2 = embeddings[1].values
    
    return cosine_similarity(vector1, vector2)
