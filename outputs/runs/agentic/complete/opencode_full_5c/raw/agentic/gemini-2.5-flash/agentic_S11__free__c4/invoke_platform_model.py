from model_client import get_text_generation_model
from model_models import ModelRequest, ModelResponse


def invoke_platform_model(request: ModelRequest) -> ModelResponse:
    model = get_text_generation_model()
    response = model.predict(prompt=request.prompt, **request.kwargs)
    return ModelResponse(text=response.text, raw_response=response._prediction_response)
