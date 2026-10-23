import os
from openai import OpenAI
from typing import Generator
import model_client
import model_models


def stream_completion(prompt: str) -> Generator[str, None, None]:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    model = model_client.get_default_model()
    system_prompt = "You are a helpful assistant."
    messages = model_models.build_messages(system_prompt, prompt)
    stream = client.chat.completions.create(
        model=model, messages=messages, stream=True, temperature=0.7
    )
    for chunk in stream:
        delta = chunk.choices[0].delta.content
        if delta is not None:
            yield delta
