import os
from openai import OpenAI
from model_client import OPENAI_API_KEY
from typing import Iterator

def stream_completion(prompt: str) -> Iterator[str]:
    """
    Streams partial output tokens from OpenAI's GPT-4.
    """
    if not OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    client = OpenAI(api_key=OPENAI_API_KEY)
    
    stream = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        stream=True,
    )
    
    for chunk in stream:
        content = chunk.choices[0].delta.content
        if content:
            yield content
