from model_client import get_openai_client
from model_models import ChatMessage
from typing import Iterator, Dict, Any


def stream_completion(prompt: str) -> Iterator[str]:
    client = get_openai_client()
    messages = [{"role": "user", "content": prompt}]
    stream = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        stream=True,
    )
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            yield chunk.choices[0].delta.content
