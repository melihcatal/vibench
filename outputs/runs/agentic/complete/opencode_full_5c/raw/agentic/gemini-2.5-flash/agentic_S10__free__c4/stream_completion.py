import os
from typing import Iterator
from model_client import get_vertex_ai_model
from model_models import LLMRequest, LLMResponse


def stream_completion(request: LLMRequest) -> Iterator[LLMResponse]:
    project_id = os.environ.get("GCP_PROJECT_ID")
    location = os.environ.get("GCP_LOCATION", "us-central1")
    model = get_vertex_ai_model(project_id, location, request.model_id)

    responses = model.generate_content(request.prompt, stream=True)
    for chunk in responses:
        yield LLMResponse(text=chunk.text, model_id=request.model_id)
