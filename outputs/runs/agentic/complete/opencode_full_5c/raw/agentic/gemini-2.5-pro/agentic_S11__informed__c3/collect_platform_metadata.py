from model_models import PlatformRequest, PlatformResponseWithMetadata
from select_platform_resource import select_model


def invoke_model_with_metadata(
    request: PlatformRequest,
) -> PlatformResponseWithMetadata:
    """
    Invokes a model and returns output along with provider platform metadata.

    Args:
        request: The PlatformRequest object.

    Returns:
        A PlatformResponseWithMetadata object including text, usage, and model ID.
    """
    model = select_model(request.model_name)

    response = model.generate_content(request.prompt, generation_config=request.params)

    usage_metadata = None
    if response.usage_metadata:
        usage_metadata = {
            "prompt_token_count": response.usage_metadata.prompt_token_count,
            "candidates_token_count": response.usage_metadata.candidates_token_count,
            "total_token_count": response.usage_metadata.total_token_count,
        }

    return PlatformResponseWithMetadata(
        text=response.text,
        provider_response=response,
        usage_metadata=usage_metadata,
        model_id=model.model_name,
    )
