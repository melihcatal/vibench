import os
import cohere
from translation_models import EmbeddingRequest, EmbeddingResponse


def translation_memory_embedding(request: EmbeddingRequest) -> EmbeddingResponse:
    """
    Generates embeddings for translated text segments using Cohere.
    """
    co = cohere.Client(os.environ.get("COHERE_API_KEY"))

    response = co.embed(
        texts=[request.text], model="embed-english-v3.0", input_type="search_document"
    )

    return EmbeddingResponse(embedding=response.embeddings[0])
