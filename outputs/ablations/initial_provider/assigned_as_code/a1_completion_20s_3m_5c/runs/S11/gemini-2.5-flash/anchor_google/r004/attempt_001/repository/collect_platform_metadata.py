from google import genai
from model_models import ModelRequest, ModelResponse

def collect_platform_metadata(model_request: ModelRequest) -> ModelResponse:
    project_id = model_request.config.get("project_id")
    location = model_request.config.get("location")
    model_name = model_request.config.get("model_name", "gemini-2.5-flash")

    client = genai.Client(vertexai=True, project=project_id, location=location)
    model = client.get_model(model_name)

    response = model.generate_content(model_request.text)

    # Extract metadata from the response object
    metadata = {
        "model": model_name,
        "project_id": project_id,
        "location": location,
        # Add other relevant metadata if available in the genai.types.GenerateContentResponse object
        "prompt_feedback": response.prompt_feedback.to_dict() if response.prompt_feedback else None,
        "usage_metadata": {
            "prompt_token_count": response.usage_metadata.prompt_token_count if response.usage_metadata else None,
            "candidates_token_count": response.usage_metadata.candidates_token_count if response.usage_metadata else None,
            "total_token_count": response.usage_metadata.total_token_count if response.usage_metadata else None,
        },
    }

    return ModelResponse(text=response.text, metadata=metadata)
