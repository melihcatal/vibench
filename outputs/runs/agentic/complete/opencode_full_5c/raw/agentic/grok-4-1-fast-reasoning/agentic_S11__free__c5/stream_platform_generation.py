from model_client import get_platform_client
from model_models import ChatMessage
from typing import List, Iterator, Dict, Any


def stream_platform_generation(
    messages: List[ChatMessage],
    deployment_id: str,
    temperature: float = 0.7,
) -> Iterator[Dict[str, Any]]:
    """
    Streams output from the managed model, yielding provider response chunk dicts.
    """
    client = get_platform_client()
    stream = client.chat.completions.create(
        model=deployment_id,
        messages=messages,
        temperature=temperature,
        stream=True,
    )
    for chunk in stream:
        yield chunk.model_dump()
