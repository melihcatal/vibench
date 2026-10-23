import os
from model_client import get_vertex_ai_model
from model_models import PlatformModelRequest, PlatformModelResponse


def stream_platform_generation(
    project_id: str, location: str, model_name: str, request: PlatformModelRequest
):
    """Streams output from a managed model platform while preserving provider response objects."""
    model = get_vertex_ai_model(project_id, location, model_name)
    responses = model.generate_content(
        contents=[request.prompt],
        generation_config={
            "max_output_tokens": request.max_output_tokens,
            "temperature": request.temperature,
        },
        stream=True,
    )

    for response in responses:
        yield PlatformModelResponse(text=response.text, raw_response=response)
