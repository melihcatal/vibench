import os
from typing import Generator
from openai import OpenAI


def stream_completion(prompt: str, model: str = "gpt-4o") -> Generator[str, None, None]:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    stream = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=2048,
        stream=True,
    )
    for chunk in stream:
        delta = chunk.choices[0].delta
        if delta.content is not None:
            yield delta.content
