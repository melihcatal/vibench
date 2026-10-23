import os
from mistralai.client import MistralClient
from typing import Iterator
from model_client import completion_prompt


def stream_completion(
    prompt: str, model: str = "mistral-large-latest"
) -> Iterator[str]:
    client = MistralClient(api_key=os.getenv("MISTRAL_API_KEY"))
    messages = [{"role": "user", "content": completion_prompt(prompt)}]
    stream = client.chat.complete(model=model, messages=messages, stream=True)
    for chunk in stream:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content
