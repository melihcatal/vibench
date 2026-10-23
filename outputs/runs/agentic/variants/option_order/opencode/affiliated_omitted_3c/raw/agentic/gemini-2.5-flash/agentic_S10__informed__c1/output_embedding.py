from model_client import ModelClient
from model_models import EmbeddingRequest, EmbeddingResponse


def get_embedding(request: EmbeddingRequest) -> EmbeddingResponse:
    client = ModelClient.get_openai_client()

    response = client.embeddings.create(input=request.text, model=request.model)

    embedding = response.data[0].embedding
    return EmbeddingResponse(embedding=embedding)
