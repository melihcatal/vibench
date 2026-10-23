from __future__ import annotations

from typing import Iterator

from openai import AzureOpenAI

from model_client import get_client, get_deployment
from model_models import PlatformRequest, PlatformResponse
from select_platform_resource import select_platform_resource


def stream_platform_generation(request: PlatformRequest) -> Iterator[object]:
    client: AzureOpenAI = get_client()
    resource = select_platform_resource()
    deployment = request.model or resource.identifier or get_deployment()
    stream = client.chat.completions.create(
        model=deployment,
        messages=[{"role": "user", "content": request.prompt}],
        temperature=request.temperature,
        max_tokens=request.max_tokens,
        stream=True,
    )
    for event in stream:
        yield event


if __name__ == "__main__":
    for chunk in stream_platform_generation(PlatformRequest(prompt="hello")):
        print(chunk)
