from typing import Iterator

from model_client import create_platform_client, load_platform_config
from model_models import PlatformRequest


def stream_platform_generation(request: PlatformRequest) -> Iterator[object]:
    config = load_platform_config()
    client = create_platform_client(config)
    return client.responses.stream(
        model=config.deployment,
        input=request.prompt,
        temperature=request.temperature,
        max_output_tokens=request.max_tokens,
    )
