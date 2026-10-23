from openai.types.chat.chat_completion import ChatCompletion
from model_client import get_platform_client
from model_models import normalize_request, ChatMessages
from typing import Any


def invoke_platform_model(
    deployment: str,
    messages: ChatMessages,
    max_tokens: int = 1024,
    temperature: float = 0.7,
    **kwargs,
) -> ChatCompletion:
    client = get_platform_client()
    request = normalize_request(
        messages, max_tokens=max_tokens, temperature=temperature, **kwargs
    )
    return client.chat.completions.create(model=deployment, **request, stream=False)
