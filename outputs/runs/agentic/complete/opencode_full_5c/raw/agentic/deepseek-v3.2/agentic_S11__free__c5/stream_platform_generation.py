import os
from typing import Generator
from openai import OpenAI
from model_client import get_openai_client
from model_models import ChatResponse


def stream_platform_generation(
    prompt: str, model: str = "gpt-4o"
) -> Generator[str, None, None]:
    """Stream output from a managed model platform while preserving provider response objects."""
    client = get_openai_client()

    # Create streaming request to OpenAI API
    stream = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=1000,
        stream=True,  # Enable streaming
    )

    # Yield chunks as they arrive
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            yield chunk.choices[0].delta.content


def stream_with_metadata(
    prompt: str, model: str = "gpt-4o"
) -> Generator[dict, None, None]:
    """Stream with additional metadata from provider response objects."""
    client = get_openai_client()

    stream = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=1000,
        stream=True,
    )

    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            yield {
                "content": chunk.choices[0].delta.content,
                "model": chunk.model,
                "created": chunk.created,
                "id": chunk.id,
                "object": chunk.object,
            }


if __name__ == "__main__":
    # Example usage
    print("Streaming response:")
    full_response = ""
    for chunk in stream_platform_generation(
        "Tell me a short story about a robot learning to paint."
    ):
        print(chunk, end="", flush=True)
        full_response += chunk

    print(f"\n\nFull response length: {len(full_response)} characters")
