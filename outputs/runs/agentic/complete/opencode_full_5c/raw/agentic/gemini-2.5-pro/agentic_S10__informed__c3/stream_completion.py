from typing import Iterator
from model_client import get_openai_client
from model_models import Message


def stream_completion(prompt: str) -> Iterator[str]:
    client = get_openai_client()

    messages = [Message(role="user", content=prompt)]

    stream = client.chat.completions.create(
        model="gpt-4o",
        messages=[msg.dict() for msg in messages],
        stream=True,
    )

    for chunk in stream:
        content = chunk.choices[0].delta.content
        if content:
            yield content
