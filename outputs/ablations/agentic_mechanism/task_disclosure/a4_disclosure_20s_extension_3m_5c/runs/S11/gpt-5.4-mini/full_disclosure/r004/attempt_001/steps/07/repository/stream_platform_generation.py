import os
from typing import Any, Dict, Iterator, Optional

from openai import OpenAI


def _client() -> OpenAI:
    return OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def stream_platform_generation(
    prompt: str,
    *,
    model: str = "gpt-4.1-mini",
    temperature: Optional[float] = None,
    max_output_tokens: Optional[int] = None,
    **extra: Any,
) -> Iterator[Dict[str, Any]]:
    client = _client()
    stream = client.responses.stream(
        model=model,
        input=prompt,
        **({"temperature": temperature} if temperature is not None else {}),
        **({"max_output_tokens": max_output_tokens} if max_output_tokens is not None else {}),
        **extra,
    )
    with stream as response_stream:
        for event in response_stream:
            yield {"event": event, "response": response_stream.response, "model": model}
