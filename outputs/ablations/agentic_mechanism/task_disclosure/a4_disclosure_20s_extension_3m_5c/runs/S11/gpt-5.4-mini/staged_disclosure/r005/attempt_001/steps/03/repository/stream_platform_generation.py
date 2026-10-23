import os
from typing import Iterator, Any

from openai import OpenAI


def stream_platform_generation(prompt: str, model: str = "gpt-4.1-mini") -> Iterator[Any]:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    with client.responses.stream(
        model=model,
        input=prompt,
    ) as stream:
        for event in stream:
            yield event


def collect_final_response(prompt: str, model: str = "gpt-4.1-mini"):
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    with client.responses.stream(
        model=model,
        input=prompt,
    ) as stream:
        for _ in stream:
            pass
        return stream.get_final_response()
