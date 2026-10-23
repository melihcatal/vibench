from typing import Iterator
from model_client import chat_completion


def stream_completion(prompt: str) -> Iterator[str]:
    messages = [{"role": "user", "content": prompt}]
    return chat_completion(messages, stream=True)
