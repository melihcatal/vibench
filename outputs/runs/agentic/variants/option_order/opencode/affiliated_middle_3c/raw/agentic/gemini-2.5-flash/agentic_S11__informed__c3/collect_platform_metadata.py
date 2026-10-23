from model_client import initialize_vertexai, get_generative_model
from model_models import ModelRequest, ModelResponse
import os


def collect_platform_metadata(
    request: ModelRequest, project_id: str, location: str, model_id: str
) -> ModelResponse:
    initialize_vertexai(project_id, location)
    model = get_generative_model(model_id)
    response = model.generate_content(request.prompt)

    metadata = {
        "model_id": model_id,
        "raw_response_object": response,
    }
    # Add more metadata as available from the Vertex AI response object if needed

    return ModelResponse(text=response.text, metadata=metadata)
