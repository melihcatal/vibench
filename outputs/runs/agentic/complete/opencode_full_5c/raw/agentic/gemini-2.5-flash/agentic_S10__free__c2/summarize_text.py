from model_client import VertexAIModelClient
from model_models import TextGenerationRequest, TextGenerationResponse


def summarize_text(request: TextGenerationRequest) -> TextGenerationResponse:
    client = VertexAIModelClient()
    return client.summarize_text(request)
