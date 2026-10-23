from model_client import get_client
from model_models import PlatformRequest, PlatformResponse, normalize_messages
from select_platform_resource import resolve_resource


def invoke_platform_model(request: PlatformRequest) -> PlatformResponse:
    client = get_client()
    resource_id, metadata = resolve_resource(request.model)
    response = client.chat.completions.create(
        model=request.model,
        messages=normalize_messages(request.prompt),
        temperature=request.temperature,
        max_tokens=request.max_tokens,
    )
    text = response.choices[0].message.content or ""
    return PlatformResponse(
        text=text,
        model=request.model,
        usage=dict(response.usage or {}),
        resource_id=resource_id,
        raw={"metadata": metadata, "response": response},
    )
