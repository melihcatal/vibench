from typing import Generator
from model_client import create_chat_completion
from model_models import ChatMessage, ChatCompletionRequest

def stream_completion(prompt: str) -> Generator[str, None, None]:
    messages = [ChatMessage(role="user", content=prompt)]
    request = ChatCompletionRequest(model="gpt-4o-mini", messages=messages)
    stream = create_chat_completion(request, stream=True)
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            yield chunk.choices[0].delta.content