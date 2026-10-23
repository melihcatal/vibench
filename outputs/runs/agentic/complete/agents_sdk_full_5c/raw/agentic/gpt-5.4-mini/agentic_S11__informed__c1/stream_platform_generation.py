from typing import Dict, Iterable, List

from model_client import build_azure_openai_client, load_platform_config
from model_models import StreamChunk, extract_stream_text
from select_platform_resource import select_platform_resource


def stream_platform_generation(messages: List[Dict[str, str]]) -> Iterable[StreamChunk]:
    config = load_platform_config()
    deployment = select_platform_resource(config.deployment)
    client = build_azure_openai_client(config)
    stream = client.chat.completions.create(
        model=deployment,
        messages=messages,
        temperature=0.2,
        max_tokens=256,
        stream=True,
    )
    for chunk in stream:
        yield StreamChunk(text=extract_stream_text(chunk), raw=chunk)
