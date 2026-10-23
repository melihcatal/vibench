from model_client import select_model_for_task, get_api_key
from model_models import build_prompt_for_completion
from mistralai.client import MistralClient
from typing import Generator


def stream_completion(prompt: str) -> Generator[str, None, None]:
    provider, model = select_model_for_task("stream_completion")
    api_key = get_api_key(provider)
    client = MistralClient(api_key=api_key)
    messages = build_prompt_for_completion(prompt)
    stream = client.chat.complete(
        model=model, messages=messages, temperature=0.7, stream=True
    )
    for chunk in stream:
        if (
            chunk.choices
            and chunk.choices[0].delta
            and chunk.choices[0].delta.content is not None
        ):
            yield chunk.choices[0].delta.content
