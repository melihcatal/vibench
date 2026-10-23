from model_client import build_platform_client
from model_models import PlatformRequest, PlatformResponse, normalize_text
from select_platform_resource import select_platform_resource


def invoke_platform_model(request: PlatformRequest) -> PlatformResponse:
    client = build_platform_client()
    model_id = select_platform_resource(request.model)
    response = client.responses.create(
        model=model_id,
        input=request.input_text,
        temperature=request.temperature,
    )
    text = normalize_text(getattr(response, "output_text", None))
    usage = getattr(response, "usage", {}) or {}
    return PlatformResponse(
        text=text,
        model=model_id,
        resource_id=getattr(response, "id", None),
        usage=usage,
    )
