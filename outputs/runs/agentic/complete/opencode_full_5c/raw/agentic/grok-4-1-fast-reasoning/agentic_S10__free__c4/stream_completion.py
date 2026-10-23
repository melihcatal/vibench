from model_client import get_llm_client, get_model_id
from typing import Generator


def stream_completion(
    prompt: str, model_family: str = "gpt-4o-mini"
) -> Generator[str, None, None]:
    client = get_llm_client()
    model = get_model_id(model_family)
    messages = [{"role": "user", "content": prompt}]
    stream = client.chat.completions.create(model=model, messages=messages, stream=True)
    for chunk in stream:
        delta = chunk.choices[0].delta.content
        if delta is not None:
            yield delta
