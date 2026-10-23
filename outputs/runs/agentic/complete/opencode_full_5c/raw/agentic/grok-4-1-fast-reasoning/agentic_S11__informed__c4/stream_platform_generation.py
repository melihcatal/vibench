from model_client import get_platform_client, get_default_deployment
from model_models import normalize_chat_request
import openai
from typing import Iterator


def stream_platform_generation(
    prompt: str, model: str = None
) -> Iterator[openai.ChatCompletionChunk]:
    client = get_platform_client()
    if model is None:
        model = get_default_deployment()
    request = normalize_chat_request(prompt, model, stream=True)
    response = client.chat.completions.create(**request)
    for chunk in response:
        yield chunk
