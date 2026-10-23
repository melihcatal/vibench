from model_client import get_cohere_client
from model_models import ModelRequest, ModelResponse


def invoke_platform_model(request: ModelRequest) -> ModelResponse:
    co = get_cohere_client()
    response = co.generate(
        prompt=request.prompt, model="command-r", temperature=request.temperature
    )

    text_generation = response.generations[0].text

    return ModelResponse(text=text_generation, metadata={"id": response.id})
