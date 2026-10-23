from typing import List
from embeddings_client import get_vertex_client
from embeddings_models import GOOGLE_EMBEDDING_MODEL

def generate_embedding(text: str) -> List[float]:
    """
    Generates an embedding for a single text string using Google Vertex AI.

    Args:
        text: The text to embed.

    Returns:
        The embedding vector.
    """
    if not text or not isinstance(text, str):
        raise ValueError("Input text must be a non-empty string.")

    client = get_vertex_client()
    embeddings = client.get_embeddings([text], model_name=GOOGLE_EMBEDDING_MODEL)
    
    return embeddings[0].values
