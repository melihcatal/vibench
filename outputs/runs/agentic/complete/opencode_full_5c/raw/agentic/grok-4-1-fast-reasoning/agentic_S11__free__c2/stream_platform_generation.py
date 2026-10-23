from openai import AzureOpenAI
from typing import Generator, Any
from model_client import get_azure_openai_config
from model_models import ModelRequest


def stream_platform_generation(request: ModelRequest) -> Generator[Any, None, None]:
    config = get_azure_openai_config()
    client = AzureOpenAI(**config)
    stream = client.chat.completions.create(
        model=request.deployment,
        messages=[msg.model_dump() for msg in request.messages],
        temperature=request.temperature,
        max_tokens=request.max_tokens,
        stream=True,
    )
    for chunk in stream:
        yield chunk
