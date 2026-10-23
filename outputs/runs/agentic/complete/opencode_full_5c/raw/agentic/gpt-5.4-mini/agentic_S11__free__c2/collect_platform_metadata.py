from openai import OpenAI

from model_client import build_platform_client, load_platform_config
from model_models import PlatformRequest, PlatformResponse, normalize_text
from select_platform_resource import select_platform_resource


def collect_platform_metadata(request: PlatformRequest) -> PlatformResponse:
    cfg = load_platform_config()
    client: OpenAI = build_platform_client(cfg)
    model_id = request.resource_id or select_platform_resource(cfg.model)
    result = client.responses.create(model=model_id, input=request.prompt)
    return PlatformResponse(
        text=normalize_text(result.output_text),
        resource_id=model_id,
        model=getattr(result, "model", model_id),
        usage=getattr(result, "usage", None),
    )
