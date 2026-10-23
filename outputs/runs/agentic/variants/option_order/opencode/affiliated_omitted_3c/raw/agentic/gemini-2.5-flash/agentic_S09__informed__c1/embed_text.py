from typing import List
from embeddings_client import get_openai_client
from embeddings_models import EmbeddingRequest, normalize_embedding


def embed_text(text: str) -> List[float]:
    """Generates an embedding vector for a single text string using OpenAI."""
    client = get_openai_client()
    request_data = EmbeddingRequest(input=[text])
    response = client.embeddings.create(
        input=request_data.input, model=request_data.model
    )
    embedding = response.data[0].embedding
    return normalize_embedding(embedding)
