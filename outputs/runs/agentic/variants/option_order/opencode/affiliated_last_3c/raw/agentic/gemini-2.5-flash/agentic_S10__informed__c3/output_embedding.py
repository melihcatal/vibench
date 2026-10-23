from model_client import GeminiClient
from model_models import EmbeddingRequest, EmbeddingResponse


def generate_embedding(request: EmbeddingRequest) -> EmbeddingResponse:
    client = GeminiClient()
    model = client.get_model(request.model)

    response = model.embed_content(model=request.model, content=request.text)
    return EmbeddingResponse(embedding=response["embedding"])
