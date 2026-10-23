from typing import List
from embeddings_client import get_openai_client
from embeddings_models import EmbeddingRequest, normalize_embedding


def embed_batch(texts: List[str]) -> List[List[float]]:
    """Generates embeddings for a batch of texts using OpenAI."""
    client = get_openai_client()
    request_data = EmbeddingRequest(input=texts)
    response = client.embeddings.create(
        input=request_data.input, model=request_data.model
    )
    embeddings = [normalize_embedding(item.embedding) for item in response.data]
    return embeddings
