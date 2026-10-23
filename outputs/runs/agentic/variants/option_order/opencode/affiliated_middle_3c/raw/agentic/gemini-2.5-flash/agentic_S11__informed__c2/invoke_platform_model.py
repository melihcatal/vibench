import os
from model_client import get_vertex_ai_model
from model_models import ModelRequest, ModelResponse


def invoke_platform_model(prompt: str) -> ModelResponse:
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    location = "us-central1"  # Example location
    model_name = "text-bison@002"  # Specific Vertex AI model

    model = get_vertex_ai_model(project_id, location, model_name)
    response = model.predict(prompt=prompt)

    return ModelResponse(text=response.text)
