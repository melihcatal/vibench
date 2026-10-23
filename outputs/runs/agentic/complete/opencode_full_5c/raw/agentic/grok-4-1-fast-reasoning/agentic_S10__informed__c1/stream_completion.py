from typing import Iterator
from model_client import get_llm_client
from model_models import MODEL_FAMILY, create_system_message, create_user_message, DEFAULT_PARAMS

def stream_completion(system_prompt: str = "", user_prompt: str) -> Iterator[str]:
    client = get_llm_client()
    messages = []
    if system_prompt:
        messages.append(create_system_message(system_prompt))
    messages.append(create_user_message(user_prompt))
    stream = client.chat.stream(
        model=MODEL_FAMILY,
        messages=messages,
        **DEFAULT_PARAMS
    )
    for chunk in stream:
        delta = chunk.choices[0].delta
        if hasattr(delta, 'content') and delta.content:
            yield delta.content