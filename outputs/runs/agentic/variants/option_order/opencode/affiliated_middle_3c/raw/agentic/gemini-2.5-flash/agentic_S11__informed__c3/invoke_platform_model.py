from model_client import initialize_vertexai, get_generative_model
from model_models import ModelRequest, ModelResponse
import os


def invoke_platform_model(
    request: ModelRequest, project_id: str, location: str, model_id: str
) -> ModelResponse:
    initialize_vertexai(project_id, location)
    model = get_generative_model(model_id)
    response = model.generate_content(request.prompt)
    return ModelResponse(text=response.text)
