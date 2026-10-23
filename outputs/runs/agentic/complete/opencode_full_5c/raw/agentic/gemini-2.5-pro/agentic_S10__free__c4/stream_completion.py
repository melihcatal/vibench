from typing import Generator
from model_client import get_openai_client


def stream_completion(prompt: str) -> Generator[str, None, None]:
    client = get_openai_client()
    stream = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        stream=True,
    )
    for chunk in stream:
        content = chunk.choices[0].delta.content
        if content:
            yield content
