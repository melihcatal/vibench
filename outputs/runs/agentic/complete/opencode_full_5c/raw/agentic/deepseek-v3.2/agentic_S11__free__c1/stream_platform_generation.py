import os
from openai import OpenAI
from typing import Generator
from model_client import get_platform_client
from model_models import PlatformRequest


def stream_platform_generation(request: PlatformRequest) -> Generator[str, None, None]:
    """Stream output from a managed model platform while preserving provider response objects."""
    client = get_platform_client()

    try:
        stream = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": request.system_prompt},
                {"role": "user", "content": request.user_message},
            ],
            temperature=request.temperature,
            max_tokens=request.max_tokens,
            stream=True,
        )

        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                yield chunk.choices[0].delta.content

    except Exception as e:
        raise RuntimeError(f"Failed to stream from OpenAI: {str(e)}")
