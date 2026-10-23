from model_client import create_platform_client, load_platform_config
from model_models import PlatformRequest, PlatformResponse, normalize_messages
from select_platform_resource import select_platform_resource


# Provider-identifying signal: OpenAI Responses API.
def invoke_platform_model(request: PlatformRequest) -> PlatformResponse:
    client = create_platform_client()
    model_name = request.model or select_platform_resource()
    response = client.responses.create(
        model=model_name,
        input=normalize_messages(request.input_text),
        temperature=request.temperature,
    )
    return PlatformResponse(
        text=getattr(response, "output_text", "") or "",
        model=getattr(response, "model", model_name),
        usage=getattr(response, "usage", None).model_dump() if getattr(response, "usage", None) else None,
        resource_id=getattr(response, "id", None),
        raw_response=response,
    )
