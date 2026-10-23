from typing import Generator
from model_client import get_openai_client
from model_models import Prompt


def stream(prompt: Prompt) -> Generator[str, None, None]:
    client = get_openai_client()
    stream = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt.text},
        ],
        stream=True,
    )
    for chunk in stream:
        content = chunk.choices[0].delta.content
        if content:
            yield content
