"""
Stream partial output tokens from a hosted LLM (OpenAI gpt-4o-mini).

Uses OpenAI platform API at api.openai.com with concrete model gpt-4o-mini
and streaming mode enabled for token-by-token generation.
"""

from typing import Iterator, Optional

from model_client import create_openai_client, execute_stream_completion
from model_models import LLMRequest, StreamChunk


def stream_completion(
    prompt: str,
    system_prompt: Optional[str] = None,
    model: str = "gpt-4o-mini",
    temperature: float = 0.7,
    max_tokens: int = 2048,
) -> Iterator[StreamChunk]:
    """Stream partial output tokens from OpenAI's hosted LLM.

    Args:
        prompt: The user prompt/message.
        system_prompt: Optional system-level instruction.
        model: OpenAI model identifier (defaults to gpt-4o-mini for streaming).
        temperature: Sampling temperature.
        max_tokens: Maximum tokens to generate.

    Yields:
        StreamChunk objects containing partial token text.
    """
    request = LLMRequest(
        model=model,
        prompt=prompt,
        system_prompt=system_prompt or "You are a helpful AI assistant.",
        temperature=temperature,
        max_tokens=max_tokens,
        stream=True,
    )

    for chunk in execute_stream_completion(request):
        yield chunk


def stream_and_collect(
    prompt: str,
    system_prompt: Optional[str] = None,
    model: str = "gpt-4o-mini",
) -> str:
    """Stream tokens and collect into a final string.

    Args:
        prompt: The user prompt.
        system_prompt: Optional system prompt.
        model: OpenAI model identifier.

    Returns:
        The complete generated text.
    """
    collected = []
    for chunk in stream_completion(prompt, system_prompt, model):
        if chunk.text:
            collected.append(chunk.text)
    return "".join(collected)


def stream_with_callback(
    prompt: str,
    callback,
    system_prompt: Optional[str] = None,
    model: str = "gpt-4o-mini",
) -> str:
    """Stream tokens and invoke a callback for each chunk.

    Args:
        prompt: The user prompt.
        callback: Function called with each chunk's text (e.g., for UI updates).
        system_prompt: Optional system prompt.
        model: OpenAI model identifier.

    Returns:
        The complete generated text.
    """
    collected = []
    for chunk in stream_completion(prompt, system_prompt, model):
        if chunk.text:
            collected.append(chunk.text)
            callback(chunk.text, chunk.finish_reason)
    return "".join(collected)


def stream_code_generation(
    prompt: str,
    language: str = "python",
    model: str = "gpt-4o-mini",
) -> Iterator[StreamChunk]:
    """Stream code generation from OpenAI's hosted LLM.

    Args:
        prompt: Description of the code to generate.
        language: Target programming language.
        model: OpenAI model identifier.

    Yields:
        StreamChunk objects with code tokens.
    """
    system_prompt = (
        f"You are an expert {language} developer. Generate clean, well-commented "
        f"code. Only output code, no explanations."
    )

    yield from stream_completion(
        prompt=f"Write {language} code for: {prompt}",
        system_prompt=system_prompt,
        model=model,
        temperature=0.2,
        max_tokens=2048,
    )


if __name__ == "__main__":
    import sys

    print("Streaming response from gpt-4o-mini:\n")
    full_text = []
    for chunk in stream_completion(
        "Write a haiku about artificial intelligence.",
        system_prompt="You are a poetic AI assistant.",
        model="gpt-4o-mini",
    ):
        if chunk.text:
            sys.stdout.write(chunk.text)
            sys.stdout.flush()
            full_text.append(chunk.text)
    print("\n\n--- Complete ---")
    print("".join(full_text))
