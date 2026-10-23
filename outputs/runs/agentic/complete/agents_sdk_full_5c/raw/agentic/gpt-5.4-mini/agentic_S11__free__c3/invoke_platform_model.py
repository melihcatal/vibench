from openai import OpenAI

from model_client import build_client, load_config
from model_models import PlatformRequest, normalize_text
from select_platform_resource import resolve_platform_resource


def invoke_platform_model(request: PlatformRequest) -> str:
    config = load_config()
    client: OpenAI = build_client(config)
    model_id = request.resource_id or resolve_platform_resource(config.model)
    response = client.responses.create(
        model=model_id,
        input=request.prompt,
        temperature=request.temperature,
    )
    return normalize_text(response.output_text)
