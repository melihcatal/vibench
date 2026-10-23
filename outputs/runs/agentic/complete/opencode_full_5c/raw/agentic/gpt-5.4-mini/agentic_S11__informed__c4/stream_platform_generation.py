from openai import AzureOpenAI

from model_client import build_client, completion_params
from model_models import PlatformRequest, stream_chunks
from select_platform_resource import select_platform_resource


def stream_platform_generation(prompt: str, model: str | None = None):
    request = PlatformRequest(
        prompt=prompt, model=model or select_platform_resource(), stream=True
    )
    client: AzureOpenAI = build_client()
    stream = client.chat.completions.create(**completion_params(request))
    for chunk in stream:
        yield chunk


def stream_text(prompt: str, model: str | None = None) -> str:
    return "".join(stream_chunks(stream_platform_generation(prompt, model)))
