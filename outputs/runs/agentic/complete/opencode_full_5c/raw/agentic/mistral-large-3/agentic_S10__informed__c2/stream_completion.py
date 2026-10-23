from typing import Iterator

from model_client import get_llm_client
from model_models import LLMRequest, LLMResponse


def stream_completion(
    prompt: str,
    model_family: str = "qwen",
    model_id: str = "qwen-turbo",
    max_tokens: int = 1000,
    temperature: float = 0.7,
) -> Iterator[str]:
    """
    Stream partial output tokens from DashScope Qwen API.
    """
    client = get_llm_client()

    request = LLMRequest(
        model_family=model_family,
        model_id=model_id,
        prompt=prompt,
        max_tokens=max_tokens,
        temperature=temperature,
        stream=True,
    )

    for chunk in client.stream(request):
        yield chunk.text
