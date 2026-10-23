from model_client import create_platform_client, load_platform_config
from model_models import PlatformRequest, PlatformResponse, normalize_text


def collect_platform_metadata(request: PlatformRequest) -> PlatformResponse:
    config = load_platform_config()
    client = create_platform_client(config)
    result = client.responses.create(model=config.deployment, input=request.prompt, temperature=request.temperature, max_output_tokens=request.max_tokens)
    return PlatformResponse(text=normalize_text(result.output), model=getattr(result, "model", None), usage=getattr(result, "usage", None), resource_id=getattr(result, "id", None))
