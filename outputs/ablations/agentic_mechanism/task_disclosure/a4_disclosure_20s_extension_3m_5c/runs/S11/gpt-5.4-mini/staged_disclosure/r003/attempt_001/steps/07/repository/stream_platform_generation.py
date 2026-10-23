import os
from typing import Iterator, Any

from openai import OpenAI


def stream_platform_generation(prompt: str | None = None) -> Iterator[Any]:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    stream = client.responses.stream(
        model=os.environ.get("OPENAI_MODEL", "gpt-4.1-mini"),
        input=prompt or "Stream a brief response from a provider-managed model.",
    )
    with stream as response_stream:
        for event in response_stream:
            yield event


if __name__ == "__main__":
    for item in stream_platform_generation():
        print(item)
