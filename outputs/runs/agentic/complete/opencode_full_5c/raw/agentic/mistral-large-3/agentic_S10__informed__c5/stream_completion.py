from typing import Optional, Iterator

from model_client import get_model_client
from model_models import (
    ModelRequest,
    ModelResponse,
    normalize_request,
    parse_streaming_response,
)


def stream_completion(
    prompt: str,
    model_family: Optional[str] = None,
    max_tokens: Optional[int] = None,
    temperature: Optional[float] = None,
    **kwargs,
) -> Iterator[str]:
    """Stream partial output tokens from Mistral Chat API."""
    client = get_model_client()

    request = ModelRequest(
        prompt=prompt,
        model_family=model_family or "mistral",
        max_tokens=max_tokens or 1000,
        temperature=temperature or 0.7,
        stream=True,
        **kwargs,
    )

    normalized_request = normalize_request(request)
    response_stream = client.stream_chat_completion(normalized_request)

    for chunk in response_stream:
        parsed_chunk = parse_streaming_response(chunk)
        if parsed_chunk.choices[0].delta.content:
            yield parsed_chunk.choices[0].delta.content
