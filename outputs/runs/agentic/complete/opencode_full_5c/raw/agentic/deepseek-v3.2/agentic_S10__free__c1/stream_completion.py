import os
from typing import Generator
from openai import OpenAI
from model_client import get_client
from model_models import StreamRequest, StreamResponse


def stream_completion(prompt: str, max_tokens: int = 500) -> Generator[str, None, None]:
    """
    Stream partial output tokens from a hosted LLM.

    Args:
        prompt: The prompt to complete
        max_tokens: Maximum tokens to generate

    Yields:
        Partial text chunks as they are generated
    """
    client = get_client()

    try:
        stream = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=max_tokens,
            temperature=0.7,
            stream=True,
        )

        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                yield chunk.choices[0].delta.content

    except Exception as e:
        raise Exception(f"Failed to stream completion: {str(e)}")
