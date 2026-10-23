from model_client import get_client
from model_models import (
    PlatformRequest,
    PlatformResponse,
    build_messages,
    extract_text_from_response,
    usage_to_dict,
)
from select_platform_resource import select_platform_resource


def invoke_platform_model(request: PlatformRequest) -> PlatformResponse:
    resource = select_platform_resource("chat", request.resource_id)
    client = get_client()
    response = client.responses.create(
        model=resource["resource_id"],
        input=build_messages(request),
        max_output_tokens=request.max_output_tokens,
        temperature=request.temperature,
    )
    return PlatformResponse(
        text=extract_text_from_response(response),
        model=resource["resource_id"],
        resource_id=resource["resource_id"],
        usage=usage_to_dict(getattr(response, "usage", None)),
        provider_response=response,
        metadata={"provider": "openai", "response_id": getattr(response, "id", None)},
    )
