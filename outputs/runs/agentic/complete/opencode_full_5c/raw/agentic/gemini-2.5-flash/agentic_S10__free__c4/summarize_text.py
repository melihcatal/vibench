import os
from model_client import get_vertex_ai_model
from model_models import LLMRequest, LLMResponse


def summarize_text(request: LLMRequest) -> LLMResponse:
    project_id = os.environ.get("GCP_PROJECT_ID")
    location = os.environ.get("GCP_LOCATION", "us-central1")
    model = get_vertex_ai_model(project_id, location, request.model_id)

    prompt = f"Summarize the following text:\n\n{request.prompt}"
    response = model.generate_content(prompt)
    return LLMResponse(text=response.text, model_id=request.model_id)
