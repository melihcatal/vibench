from model_client import get_azure_openai_client
from model_models import (
    GenerationRequest,
    GenerationResult,
    first_text_from_chat_response,
    usage_to_dict,
)
from select_platform_resource import select_platform_resource


def invoke_platform_model(request: GenerationRequest) -> GenerationResult:
    resource = select_platform_resource(request)
    client = get_azure_openai_client()
    response = client.chat.completions.create(
        model=resource.azure_deployment,
        messages=request.to_chat_messages(),
        temperature=request.temperature,
        max_tokens=request.max_tokens,
    )
    return GenerationResult(
        text=first_text_from_chat_response(response),
        model=getattr(response, "model", resource.model_family),
        usage=usage_to_dict(getattr(response, "usage", None)),
        resource={
            "azure_deployment": resource.azure_deployment,
            "model_family": resource.model_family,
        },
        raw_response=response,
    )
