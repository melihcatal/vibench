from typing import Any, Dict

from openai import OpenAI

from model_client import build_client, load_config
from model_models import PlatformRequest, PlatformResponse, normalize_text
from select_platform_resource import resolve_platform_resource


def collect_platform_metadata(request: PlatformRequest) -> PlatformResponse:
    config = load_config()
    client: OpenAI = build_client(config)
    model_id = request.resource_id or resolve_platform_resource(config.model)
    response = client.responses.create(
        model=model_id,
        input=request.prompt,
        temperature=request.temperature,
    )
    usage: Dict[str, Any] = {}
    if getattr(response, "usage", None) is not None:
        usage = response.usage.model_dump() if hasattr(response.usage, "model_dump") else dict(response.usage)
    return PlatformResponse(
        text=normalize_text(response.output_text),
        model=model_id,
        usage=usage or None,
        resource_id=model_id,
        raw=response,
    )
