from typing import List, Dict, Any, Generator

from .model_client import get_azure_openai_client


def stream_platform_generation(
    messages: List[Dict[str, str]], deployment: str, **kwargs: Any
) -> Generator[Any, None, None]:
    client = get_azure_openai_client(deployment)
    stream = client.chat.completions.create(messages=messages, stream=True, **kwargs)
    for chunk in stream:
        yield chunk
