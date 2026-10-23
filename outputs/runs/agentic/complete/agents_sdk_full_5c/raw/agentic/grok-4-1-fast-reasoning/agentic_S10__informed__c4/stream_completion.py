from typing import Generator
from model_client import get_client, MODEL_NAME
from model_models import stream_tokens

def stream_completion(prompt: str) -> Generator[str, None, None]:
    client = get_client()
    messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages,
        stream=True,
        max_tokens=1000,
    )
    yield from stream_tokens(response)
