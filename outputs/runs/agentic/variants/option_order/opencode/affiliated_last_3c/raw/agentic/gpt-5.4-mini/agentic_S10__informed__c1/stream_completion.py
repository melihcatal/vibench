from typing import Iterator

from openai import OpenAI

from model_client import build_messages, get_model_name, get_openai_client
from model_models import normalize_text


def stream_completion(prompt: str) -> Iterator[str]:
    client: OpenAI = get_openai_client()
    response = client.chat.completions.create(
        model=get_model_name(),
        messages=build_messages("Stream a helpful completion.", normalize_text(prompt)),
        temperature=0.2,
        stream=True,
    )
    for chunk in response:
        delta = chunk.choices[0].delta.content if chunk.choices else None
        if delta:
            yield delta
