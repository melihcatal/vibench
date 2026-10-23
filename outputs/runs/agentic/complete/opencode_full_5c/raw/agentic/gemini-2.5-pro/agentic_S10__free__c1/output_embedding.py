from model_client import get_model_client
from model_models import EmbeddingRequest, EmbeddingResponse


def get_output_embedding(request: EmbeddingRequest) -> EmbeddingResponse:
    cohere_client = get_model_client()

    response = cohere_client.embed(
        texts=request.texts, model=request.model, input_type=request.input_type
    )

    return EmbeddingResponse(embeddings=response.embeddings)
