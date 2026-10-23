from typing import Iterator

from model_client import build_platform_client, load_platform_config
from select_platform_resource import select_platform_resource


def stream_platform_generation(prompt: str) -> Iterator[object]:
    config = load_platform_config()
    client = build_platform_client(config)
    deployment = select_platform_resource(config.deployment)
    stream = client.chat.completions.create(
        model=deployment,
        messages=[{"role": "user", "content": prompt}],
        stream=True,
    )
    for event in stream:
        yield event
