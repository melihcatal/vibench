import os
from model_client import get_vertex_ai_model
from model_models import PlatformModelRequest, PlatformModelResponse


def invoke_platform_model(
    project_id: str, location: str, model_name: str, request: PlatformModelRequest
) -> PlatformModelResponse:
    """Invokes a provider-managed model through a project-scoped platform client."""
    model = get_vertex_ai_model(project_id, location, model_name)
    responses = model.generate_content(
        contents=[request.prompt],
        generation_config={
            "max_output_tokens": request.max_output_tokens,
            "temperature": request.temperature,
        },
    )
    text_output = responses.text
    return PlatformModelResponse(text=text_output, raw_response=responses)
