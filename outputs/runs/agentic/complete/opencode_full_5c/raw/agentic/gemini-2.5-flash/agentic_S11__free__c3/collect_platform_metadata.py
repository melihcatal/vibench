import vertexai
from vertexai.preview.generative_models import GenerativeModel, Part, GenerationConfig
from model_client import get_vertex_ai_project_location
from model_models import PlatformInvocationRequest, PlatformMetadataResponse


def collect_platform_metadata(
    request: PlatformInvocationRequest,
) -> PlatformMetadataResponse:
    project, location = get_vertex_ai_project_location()
    vertexai.init(project=project, location=location)

    model = GenerativeModel(request.model_id)
    generation_config = GenerationConfig(
        temperature=request.temperature,
        max_output_tokens=request.max_output_tokens,
    )

    prompt_parts = [Part.from_text(request.prompt)]

    response = model.generate_content(prompt_parts, generation_config=generation_config)

    # Vertex AI responses contain usage metadata
    usage_metadata = (
        response.usage_metadata if hasattr(response, "usage_metadata") else None
    )

    return PlatformMetadataResponse(
        output=response.text,
        model_id=request.model_id,
        provider="Google Cloud Vertex AI",
        input_token_count=usage_metadata.prompt_token_count if usage_metadata else None,
        output_token_count=usage_metadata.candidates_token_count
        if usage_metadata
        else None,
        total_token_count=usage_metadata.total_token_count if usage_metadata else None,
        # Other metadata can be extracted from response object if available and relevant
        raw_response_object=response,
    )
