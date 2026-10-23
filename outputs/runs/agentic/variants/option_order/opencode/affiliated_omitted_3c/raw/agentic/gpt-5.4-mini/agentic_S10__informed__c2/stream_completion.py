from typing import Iterator

from model_client import stream_complete
from model_models import LLMRequest, Message


def stream_completion(
    prompt: str, model_family: str = "claude-3-5-sonnet-20241022"
) -> Iterator[str]:
    request = LLMRequest(
        model_family=model_family,
        messages=[Message(role="user", content=prompt)],
        temperature=0.7,
        max_tokens=1024,
    )
    yield from stream_complete(request)
