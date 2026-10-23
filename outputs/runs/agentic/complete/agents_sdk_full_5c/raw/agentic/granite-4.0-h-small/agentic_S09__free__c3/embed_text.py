import os
from embeddings_client import get_client
from embeddings_models import normalize_embedding

def embed_text(text: str) -> list[float]:
    """Generate an embedding vector for a single text using the Direct Embeddings API.
    
    Returns:
        List of float values representing the embedding.
    """
    client = get_client()
    # Provider-specific model identifier (e.g., OpenAI's ada-002)
    model_id = "text-embedding-ada-002"
    response = client.create_embedding(
        model=model_id,
        input=text,
        # optional parameters such as dimensions can be added here
    )
    # Assume the API returns JSON with a field 'embedding' containing the vector
    embedding = response["embedding"]
    return normalize_embedding(embedding)
