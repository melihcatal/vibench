from model_client import get_cohere_client
from model_models import ModelRequest, ModelResponse


def invoke_model_with_metadata(request: ModelRequest) -> ModelResponse:
    cohere_client = get_cohere_client()

    response = cohere_client.chat(model=request.model, message=request.prompt)

    metadata = {
        "api_version": response.meta["api_version"],
        "billed_units": response.meta["billed_units"],
        "tokens": response.meta.get("tokens"),
    }

    return ModelResponse(text=response.text, metadata=metadata)
