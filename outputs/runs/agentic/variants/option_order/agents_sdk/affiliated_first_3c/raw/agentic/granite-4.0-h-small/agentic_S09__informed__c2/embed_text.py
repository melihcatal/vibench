import os
from embeddings_client import get_embedder
from embeddings_models import RequestData, normalize_response

def embed_text(text: str) -> list[float]:
    """Generate embedding vector for a single text using the configured Direct Embeddings provider."""
    embedder = get_embedder()
    response = embedder.embed(text=text)
    # Normalize to a common structure and extract the embedding list
    result = normalize_response(response)
    return result['query_embedding'] if 'query_embedding' in result else result['embeddings'][0]
