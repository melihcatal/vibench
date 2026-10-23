import os
from model_client import get_vertex_model
from model_models import ModelRequest, ModelResponse


def collect_vertex_metadata(request: ModelRequest) -> ModelResponse:
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    location = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")
    model_name = os.environ.get("VERTEX_AI_MODEL_NAME", "gemini-pro")

    model = get_vertex_model(project_id, location, model_name)
    response = model.generate_content(request.prompt, **request.kwargs)

    # Provider-identifying signal: response.usage_metadata and response.candidates are specific to Vertex AI SDK response objects
    metadata = {
        "usage_metadata": response.usage_metadata,
        "candidates_finish_reasons": [c.finish_reason for c in response.candidates],
        "model_name": model_name,
        "project_id": project_id,
        "location": location,
    }

    return ModelResponse(text=response.text, metadata=metadata)
