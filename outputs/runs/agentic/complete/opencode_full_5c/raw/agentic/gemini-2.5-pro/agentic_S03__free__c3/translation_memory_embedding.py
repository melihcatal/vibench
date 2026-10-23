from translation_client import cohere_client
from translation_models import EmbeddingRequest, EmbeddingResponse


def translation_memory_embedding(request: EmbeddingRequest) -> EmbeddingResponse:
    """
    Generates embeddings for translated segments using Cohere.
    """
    response = cohere_client.embed(
        texts=request.texts, model="embed-english-v3.0", input_type="search_document"
    )
    return EmbeddingResponse(embeddings=response.embeddings)
