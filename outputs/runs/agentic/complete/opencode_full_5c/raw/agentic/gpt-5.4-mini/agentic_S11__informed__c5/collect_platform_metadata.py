from model_client import get_client
from model_models import PlatformRequest, PlatformResponse, normalize_messages
from select_platform_resource import resolve_resource


def collect_platform_metadata(request: PlatformRequest) -> PlatformResponse:
    client = get_client()
    resource_id, metadata = resolve_resource(request.model)
    response = client.chat.completions.create(
        model=request.model,
        messages=normalize_messages(request.prompt),
        temperature=request.temperature,
        max_tokens=request.max_tokens,
    )
    return PlatformResponse(
        text=response.choices[0].message.content or "",
        model=request.model,
        usage=dict(response.usage or {}),
        resource_id=resource_id,
        raw={
            "metadata": metadata,
            "response_id": getattr(response, "id", None),
            "model": getattr(response, "model", request.model),
        },
    )
