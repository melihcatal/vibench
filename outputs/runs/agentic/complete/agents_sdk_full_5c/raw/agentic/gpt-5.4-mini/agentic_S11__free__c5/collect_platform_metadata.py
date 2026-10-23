from model_client import create_platform_client
from model_models import PlatformRequest, PlatformResponse, normalize_messages
from select_platform_resource import select_platform_resource


# Provider-identifying signal: OpenAI usage metadata and response IDs.
def collect_platform_metadata(request: PlatformRequest) -> PlatformResponse:
    client = create_platform_client()
    model_name = request.model or select_platform_resource()
    response = client.responses.create(
        model=model_name,
        input=normalize_messages(request.input_text),
        temperature=request.temperature,
    )
    usage = getattr(response, "usage", None)
    return PlatformResponse(
        text=getattr(response, "output_text", "") or "",
        model=getattr(response, "model", model_name),
        usage=usage.model_dump() if usage else None,
        resource_id=getattr(response, "id", None),
        raw_response=response,
    )
