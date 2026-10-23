from typing import Generator
import os
from model_client import get_llm_client, get_model
from model_models import build_completion_prompt

def stream_completion(prompt: str, model_family: str = "mini") -> Generator[str, None, None]:
    client = get_llm_client()
    model = get_model(model_family)
    stream = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": build_completion_prompt(prompt)}],
        stream=True,
        temperature=0.7,
    )
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            yield chunk.choices[0].delta.content
