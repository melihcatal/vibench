import os
from typing import Iterator
from openai import OpenAI

from model_client import build_messages, get_model_name
from model_models import normalize_text

STREAM_MODEL = get_model_name(os.getenv("STREAM_MODEL", "gpt-4.1-mini"))


def stream_completion(prompt: str) -> Iterator[str]:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"), base_url=os.getenv("OPENAI_BASE_URL"))
    stream = client.chat.completions.create(
        model=STREAM_MODEL,
        messages=build_messages(
            "You are a streaming assistant powered by OpenAI chat completions.",
            prompt,
        ),
        temperature=0.2,
        stream=True,
    )
    for chunk in stream:
        delta = getattr(chunk.choices[0].delta, "content", None)
        if delta:
            yield normalize_text(delta)
