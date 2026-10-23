import os
from typing import Generator
from openai import OpenAI
from model_client import get_client
from model_models import StreamRequest, StreamChunk


def stream_completion(prompt: str) -> Generator[str, None, None]:
    """
    Stream partial output tokens from a hosted LLM.
    """
    client = get_client()

    try:
        stream = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ],
            stream=True,
            temperature=0.7,
            max_tokens=500,
        )

        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                yield chunk.choices[0].delta.content
    except Exception as e:
        raise Exception(f"Failed to stream completion: {str(e)}")
