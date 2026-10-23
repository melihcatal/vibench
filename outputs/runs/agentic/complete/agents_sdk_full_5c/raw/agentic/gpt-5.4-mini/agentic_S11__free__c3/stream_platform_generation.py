from typing import Iterator

from openai import OpenAI

from model_client import build_client, load_config
from model_models import PlatformRequest
from select_platform_resource import resolve_platform_resource


def stream_platform_generation(request: PlatformRequest) -> Iterator[object]:
    config = load_config()
    client: OpenAI = build_client(config)
    model_id = request.resource_id or resolve_platform_resource(config.model)
    with client.responses.stream(
        model=model_id,
        input=request.prompt,
        temperature=request.temperature,
    ) as stream:
        for event in stream:
            yield event
        yield stream.get_final_response()
