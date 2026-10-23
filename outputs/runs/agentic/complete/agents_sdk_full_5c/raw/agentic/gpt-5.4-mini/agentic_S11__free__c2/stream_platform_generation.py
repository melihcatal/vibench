import os
from typing import Iterator

from openai import OpenAI

from model_client import get_openai_client, get_model_name


def stream_platform_generation(prompt: str) -> Iterator[object]:
    client: OpenAI = get_openai_client()
    model = get_model_name(default="gpt-4.1-mini")
    stream = client.responses.create(model=model, input=prompt, stream=True)
    for event in stream:
        yield event


if __name__ == "__main__":
    prompt = os.environ.get("MODEL_PROMPT", "Stream a short platform update.")
    for event in stream_platform_generation(prompt):
        print(event)
