from model_client import get_azure_openai_client
from model_models import ModelRequest
from select_platform_resource import select_platform_resource
from typing import Iterator


def stream_platform_generation(
    request: ModelRequest, model_family: str = "gpt-4o"
) -> Iterator:
    client = get_azure_openai_client()
    deployment = select_platform_resource(model_family)
    openai_request = {
        "model": deployment,
        "messages": request["messages"],
        "stream": True,
    }
    stream = client.chat.completions.create(**openai_request)
    for chunk in stream:
        yield chunk
