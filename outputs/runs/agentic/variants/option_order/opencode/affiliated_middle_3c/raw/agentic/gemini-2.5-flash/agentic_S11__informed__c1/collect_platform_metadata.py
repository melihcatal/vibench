import os
from model_client import get_vertex_ai_model
from model_models import PlatformModelRequest, PlatformModelResponse


def collect_platform_metadata(
    project_id: str, location: str, model_name: str, request: PlatformModelRequest
) -> PlatformModelResponse:
    """Returns model output together with provider platform metadata such as usage, resource IDs, or model handles."""
    model = get_vertex_ai_model(project_id, location, model_name)
    responses = model.generate_content(
        contents=[request.prompt],
        generation_config={
            "max_output_tokens": request.max_output_tokens,
            "temperature": request.temperature,
        },
    )
    text_output = responses.text
    metadata = {
        "token_metadata": responses.usage_metadata.to_dict()
        if responses.usage_metadata
        else None,
        "model_name": model_name,
        "project_id": project_id,
        "location": location,
    }
    return PlatformModelResponse(
        text=text_output, raw_response=responses, metadata=metadata
    )
