import os
from typing import Generator
from openai import OpenAI


def stream_platform_generation(
    prompt: str, model: str = "gpt-4o"
) -> Generator[str, None, None]:
    """
    Streams output from a managed model platform while preserving provider response objects.
    Uses OpenAI's streaming API to yield tokens as they're generated.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")

    client = OpenAI(api_key=api_key)

    stream = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1000,
        temperature=0.7,
        stream=True,
    )

    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            yield chunk.choices[0].delta.content
