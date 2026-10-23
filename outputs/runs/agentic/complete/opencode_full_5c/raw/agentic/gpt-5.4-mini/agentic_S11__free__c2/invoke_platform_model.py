from openai import OpenAI

from model_client import build_platform_client, load_platform_config
from model_models import PlatformRequest, normalize_text
from select_platform_resource import select_platform_resource


def invoke_platform_model(request: PlatformRequest) -> str:
    cfg = load_platform_config()
    client: OpenAI = build_platform_client(cfg)
    model_id = request.resource_id or select_platform_resource(cfg.model)
    result = client.responses.create(model=model_id, input=request.prompt)
    return normalize_text(result.output_text)
