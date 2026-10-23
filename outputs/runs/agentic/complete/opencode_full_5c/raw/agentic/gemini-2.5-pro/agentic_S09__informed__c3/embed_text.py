from typing import List
from embeddings_client import get_openai_client
from embeddings_models import EmbeddingRequest


def generate_embedding(text: str) -> List[float]:
    """
    Generates an embedding vector for a single text string using OpenAI.
    """
    client = get_openai_client()
    request = EmbeddingRequest(input=text)
    response = client.embeddings.create(input=request.input, model=request.model)
    return response.data[0].embedding
