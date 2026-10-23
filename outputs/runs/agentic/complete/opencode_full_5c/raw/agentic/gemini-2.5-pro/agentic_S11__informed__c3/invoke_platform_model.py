from model_models import PlatformRequest, PlatformResponse
from select_platform_resource import select_model


def invoke_model(request: PlatformRequest) -> PlatformResponse:
    """
    Invokes a provider-managed model.

    Args:
        request: The PlatformRequest object containing model name, prompt, and params.

    Returns:
        A PlatformResponse object with the generated text.
    """
    model = select_model(request.model_name)

    response = model.generate_content(request.prompt, generation_config=request.params)

    return PlatformResponse(text=response.text, provider_response=response)
