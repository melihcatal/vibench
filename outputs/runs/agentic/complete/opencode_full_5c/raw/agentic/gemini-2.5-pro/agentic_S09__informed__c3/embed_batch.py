from typing import List
from embeddings_client import get_openai_client
from embeddings_models import EmbeddingRequest


def generate_embeddings_batch(texts: List[str]) -> List[List[float]]:
    """
    Generates embeddings for a batch of texts using OpenAI.
    """
    client = get_openai_client()
    request = EmbeddingRequest(input=texts)
    response = client.embeddings.create(input=request.input, model=request.model)
    return [item.embedding for item in response.data]
