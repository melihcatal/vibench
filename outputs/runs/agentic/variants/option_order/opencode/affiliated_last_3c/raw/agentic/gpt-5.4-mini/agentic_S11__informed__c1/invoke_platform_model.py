from model_client import deployment_name, get_client, load_config
from model_models import PlatformRequest, PlatformResponse, extract_text, response_usage
from select_platform_resource import select_platform_resource


def invoke_platform_model(
    request: PlatformRequest, resource: str | None = None
) -> PlatformResponse:
    cfg = load_config()
    client = get_client()
    deployment = select_platform_resource(resource)
    response = client.chat.completions.create(
        model=deployment,
        messages=[{"role": "user", "content": request.prompt}],
        temperature=request.temperature,
        max_tokens=request.max_tokens,
    )
    return PlatformResponse(
        text=extract_text(response),
        model=cfg.model,
        resource_id=deployment,
        usage=response_usage(response),
        raw=response,
    )
