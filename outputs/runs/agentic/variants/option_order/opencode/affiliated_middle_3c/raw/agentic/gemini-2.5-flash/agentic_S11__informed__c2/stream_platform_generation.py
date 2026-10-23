import os
from typing import Iterator
from model_client import get_vertex_ai_model
from model_models import ModelResponse


def stream_platform_generation(prompt: str) -> Iterator[ModelResponse]:
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    location = "us-central1"  # Example location
    model_name = "text-bison@002"  # Specific Vertex AI model

    model = get_vertex_ai_model(project_id, location, model_name)

    responses = model.predict_streaming(prompt=prompt)
    for response in responses:
        yield ModelResponse(text=response.text)
