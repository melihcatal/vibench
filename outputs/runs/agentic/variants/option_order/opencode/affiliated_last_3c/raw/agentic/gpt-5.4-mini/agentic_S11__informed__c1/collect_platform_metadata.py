from model_client import load_config
from model_models import PlatformRequest, PlatformResponse
from invoke_platform_model import invoke_platform_model


def collect_platform_metadata(
    request: PlatformRequest, resource: str | None = None
) -> PlatformResponse:
    response = invoke_platform_model(request, resource=resource)
    cfg = load_config()
    return PlatformResponse(
        text=response.text,
        model=cfg.model,
        resource_id=response.resource_id,
        usage=response.usage,
        raw=response.raw,
    )
