import os
from openai import OpenAI
from typing import Iterator

def stream_completion(prompt: str) -> Iterator[str]:
    """
    Streams partial output tokens from a hosted LLM (OpenAI).
    """
    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")
    )

    stream = client.chat.completions.create(
        model="gpt-4o", # Using a concrete model identifier
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        stream=True
    )
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            yield chunk.choices[0].delta.content