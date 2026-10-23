import vertexai
from vertexai.generative_models import GenerativeModel, Part
from model_client import initialize_vertex_ai
from model_models import ModelRequest, ModelResponse
import os


def collect_platform_metadata(
    request: ModelRequest, model_name: str = "gemini-pro"
) -> ModelResponse:
    """Returns model output together with provider platform metadata such as usage, resource IDs, or model handles."""
    project_id, location = initialize_vertex_ai()

    model = GenerativeModel(model_name)
    response = model.generate_content(request.prompt, generation_config=request.params)

    # Collect metadata
    metadata = {
        "model_name": model_name,
        "project_id": project_id,
        "location": location,
        "finish_reason": response.candidates[0].finish_reason.name
        if response.candidates
        else None,
        "prompt_token_count": response.usage_metadata.prompt_token_count
        if response.usage_metadata
        else None,
        "candidates_token_count": response.usage_metadata.candidates_token_count
        if response.usage_metadata
        else None,
        "total_token_count": response.usage_metadata.total_token_count
        if response.usage_metadata
        else None,
    }

    return ModelResponse(text=response.text, metadata=metadata)
