from embeddings_client import get_cohere_client
from embeddings_models import EmbeddingResponse


def embed_text(text: str) -> EmbeddingResponse:
    """
    Generates an embedding vector for one text string using Cohere API.
    """
    cohere_client = get_cohere_client()
    model = "embed-english-v3.0"
    response = cohere_client.embed(
        texts=[text], model=model, input_type="search_document"
    )
    return EmbeddingResponse(embeddings=response.embeddings, model=model)
