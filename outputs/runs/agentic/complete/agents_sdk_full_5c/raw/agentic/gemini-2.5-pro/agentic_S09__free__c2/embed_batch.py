from typing import List
from embeddings_client import get_vertex_client
from embeddings_models import GOOGLE_EMBEDDING_MODEL, EmbeddingResponse

def generate_embeddings_batch(texts: List[str]) -> List[EmbeddingResponse]:
    """
    Generates embeddings for a batch of text strings using Google Vertex AI.

    Args:
        texts: A list of texts to embed.

    Returns:
        A list of EmbeddingResponse objects.
    """
    if not texts or not all(isinstance(t, str) for t in texts):
        raise ValueError("Input must be a non-empty list of strings.")

    client = get_vertex_client()
    # The API supports up to 250 texts per call for this model
    embeddings = client.get_embeddings(texts, model_name=GOOGLE_EMBEDDING_MODEL)
    
    responses = [
        EmbeddingResponse(text=embedding.text, vector=embedding.values)
        for embedding in embeddings
    ]
    return responses
