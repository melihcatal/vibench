from typing import Iterator

from model_client import create_chat_completion
from model_models import stream_content, ChatMessages

def stream_completion(prompt: str) -> Iterator[str]:
    messages: ChatMessages = [{"role": "user", "content": prompt}]
    stream = create_chat_completion(messages, stream=True)
    return stream_content(stream)