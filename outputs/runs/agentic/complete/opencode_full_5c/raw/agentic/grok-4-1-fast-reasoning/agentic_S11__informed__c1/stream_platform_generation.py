from model_client import get_client
from typing import Iterator, Any, List, Dict


def stream_platform_generation(
    messages: List[Dict[str, str]], deployment_id: str
) -> Iterator[Any]:
    client = get_client()
    stream = client.chat.completions.create(
        model=deployment_id,
        messages=messages,
        stream=True,
    )
    for chunk in stream:
        yield chunk
