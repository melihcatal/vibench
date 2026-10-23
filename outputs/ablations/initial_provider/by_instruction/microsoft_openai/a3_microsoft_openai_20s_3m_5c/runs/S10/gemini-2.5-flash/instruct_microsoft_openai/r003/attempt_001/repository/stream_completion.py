import os
from openai import OpenAI
from typing import Iterator

def stream_completion(prompt: str) -> Iterator[str]:
    """
    Streams partial output tokens from a hosted LLM (OpenAI's GPT-3.5 Turbo).
    """
    client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY"),
    )

    stream = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ],
        stream=True,
    )

    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            yield chunk.choices[0].delta.content
