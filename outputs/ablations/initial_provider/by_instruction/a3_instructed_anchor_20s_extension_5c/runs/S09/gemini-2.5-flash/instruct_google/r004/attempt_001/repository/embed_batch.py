from typing import List
from embeddings_client import EmbeddingsClient
from embeddings_models import EmbeddingsModels

def embed_batch(texts: List[str]) -> List[List[float]]:
    """Generates embeddings for a batch of text strings using Google Vertex AI.

    Args:
        texts: A list of text strings to embed.

    Returns:
        A list of embedding vectors, where each vector is a list of floats.
    """
    client = EmbeddingsClient()
    instances = EmbeddingsModels.prepare_instances(texts)
    
    response = client.get_client().predict(endpoint=client.get_endpoint(), instances=instances)
    
    return EmbeddingsModels.parse_response(response)
