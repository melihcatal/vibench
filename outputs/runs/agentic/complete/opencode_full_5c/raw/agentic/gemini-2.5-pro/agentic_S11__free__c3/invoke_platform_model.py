from model_client import get_cohere_client
from model_models import ModelRequest, ModelResponse


def invoke_model(request: ModelRequest) -> ModelResponse:
    cohere_client = get_cohere_client()

    response = cohere_client.chat(model=request.model, message=request.prompt)

    return ModelResponse(text=response.text)
