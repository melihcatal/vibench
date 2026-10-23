import vertexai
from vertexai.preview.generative_models import GenerativeModel, Part, GenerationConfig
from model_client import get_vertex_ai_project_location
from model_models import PlatformInvocationRequest, PlatformStreamingResponse


def stream_platform_generation(request: PlatformInvocationRequest):
    project, location = get_vertex_ai_project_location()
    vertexai.init(project=project, location=location)

    model = GenerativeModel(request.model_id)
    generation_config = GenerationConfig(
        temperature=request.temperature,
        max_output_tokens=request.max_output_tokens,
    )

    prompt_parts = [Part.from_text(request.prompt)]

    responses = model.generate_content(
        prompt_parts, generation_config=generation_config, stream=True
    )

    for response in responses:
        yield PlatformStreamingResponse(
            chunk=response.text,
            model_id=request.model_id,
            provider="Google Cloud Vertex AI",
            raw_response_object=response,  # Preserve the original response object
        )
