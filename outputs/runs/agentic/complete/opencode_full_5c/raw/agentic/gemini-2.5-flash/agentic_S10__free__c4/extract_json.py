import os
import json
from model_client import get_vertex_ai_model
from model_models import LLMRequest, LLMResponse


def extract_json(request: LLMRequest) -> LLMResponse:
    project_id = os.environ.get("GCP_PROJECT_ID")
    location = os.environ.get("GCP_LOCATION", "us-central1")
    model = get_vertex_ai_model(project_id, location, request.model_id)

    prompt = f"Extract structured JSON from the following text. The JSON should represent key entities and their attributes. If no structured data is found, return an empty JSON object:\n\n{request.prompt}"
    response = model.generate_content(prompt)

    # Attempt to parse the response as JSON. If it fails, return the raw text.
    try:
        json_output = json.loads(response.text)
        return LLMResponse(
            text=json.dumps(json_output, indent=2), model_id=request.model_id
        )
    except json.JSONDecodeError:
        return LLMResponse(text=response.text, model_id=request.model_id)
