from model_client import openai_client
from typing import Generator


def stream_completion(prompt: str) -> Generator[str, None, None]:
    stream = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        stream=True,
        temperature=0.7,
    )
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            yield chunk.choices[0].delta.content
