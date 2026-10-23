from typing import Generator
from model_client import get_openai_client, get_model
from model_models import build_chat_messages


def stream_completion(prompt: str) -> Generator[str, None, None]:
    client = get_openai_client()
    model = get_model()
    messages = build_chat_messages(user_prompt=prompt)
    stream = client.chat.completions.create(model=model, messages=messages, stream=True)
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            yield chunk.choices[0].delta.content
