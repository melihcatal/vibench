"""
Stream partial output tokens from a hosted OpenAI LLM.
Provider: OpenAI Chat Completions API with streaming (model: gpt-4o)
SDK: openai
Auth: OPENAI_API_KEY
"""

from typing import Optional, Iterator, Callable
from model_client import get_client, DEFAULT_MODEL
from model_models import (
    StreamingChunk,
    normalize_streaming_output,
)


def stream_completion(
    system_prompt: str,
    user_prompt: str,
    model: str = DEFAULT_MODEL,
    temperature: float = 0.7,
    max_tokens: Optional[int] = None,
    on_chunk: Optional[Callable[[str], None]] = None,
) -> str:
    """
    Stream partial output tokens from the OpenAI hosted LLM.

    Args:
        system_prompt: The system prompt for the conversation.
        user_prompt: The user prompt/question.
        model: OpenAI model identifier (e.g., "gpt-4o", "gpt-4o-mini").
        temperature: Sampling temperature.
        max_tokens: Maximum tokens to generate.
        on_chunk: Optional callback invoked for each streamed chunk.

    Returns:
        The complete streamed output as a string.
    """
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]
    client = get_client()

    stream = client.create_streaming_completion(
        messages=messages,
        model=model,
        temperature=temperature,
        max_tokens=max_tokens,
    )

    full_output = []
    for chunk in stream:
        parsed = StreamingChunk.from_openai_chunk(chunk)
        if parsed and parsed.delta_content:
            full_output.append(parsed.delta_content)
            if on_chunk:
                on_chunk(parsed.delta_content)

    return "".join(full_output)


def stream_completion_generator(
    system_prompt: str,
    user_prompt: str,
    model: str = DEFAULT_MODEL,
    temperature: float = 0.7,
    max_tokens: Optional[int] = None,
) -> Iterator[StreamingChunk]:
    """
    Stream completion as a generator of StreamingChunk objects.

    Args:
        system_prompt: The system prompt.
        user_prompt: The user prompt.
        model: OpenAI model identifier.
        temperature: Sampling temperature.
        max_tokens: Maximum tokens to generate.

    Yields:
        StreamingChunk objects for each received chunk.
    """
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]
    client = get_client()

    stream = client.create_streaming_completion(
        messages=messages,
        model=model,
        temperature=temperature,
        max_tokens=max_tokens,
    )

    for chunk in stream:
        parsed = StreamingChunk.from_openai_chunk(chunk)
        if parsed is not None:
            yield parsed


def stream_code_generation(
    prompt: str,
    language: str = "python",
    model: str = DEFAULT_MODEL,
) -> str:
    """
    Stream code generation with a language-specific system prompt.

    Args:
        prompt: The code generation prompt.
        language: The target programming language.
        model: OpenAI model identifier.

    Returns:
        Generated code as a string.
    """
    system_prompt = f"You are an expert {language} programmer. Write clean, well-documented {language} code. Only output the code, no explanations."
    return stream_completion(
        system_prompt=system_prompt,
        user_prompt=prompt,
        model=model,
        temperature=0.2,
    )


if __name__ == "__main__":
    import os
    import sys
    if not os.environ.get("OPENAI_API_KEY"):
        print("OPENAI_API_KEY environment variable is required.")
    else:
        print("Streaming response (tokens arrive in real-time):\n")

        def print_token(token: str):
            sys.stdout.write(token)
            sys.stdout.flush()

        result = stream_completion(
            system_prompt="You are a helpful assistant.",
            user_prompt="Explain what a closure is in Python in 3 sentences.",
            on_chunk=print_token,
        )
        print(f"\n\nFinal output:\n{result}")
