from embeddings_client import get_cohere_client
from embeddings_models import EmbeddingResponse


def generate_embedding(text: str) -> EmbeddingResponse:
    """
    Generates an embedding vector for a single text string using Cohere.
    """
    cohere_client = get_cohere_client()
    response = cohere_client.embed(
        texts=[text], model="embed-english-v3.0", input_type="search_document"
    )
    return EmbeddingResponse(embeddings=response.embeddings)
