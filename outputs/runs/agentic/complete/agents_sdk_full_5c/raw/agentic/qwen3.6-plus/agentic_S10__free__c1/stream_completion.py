"""
stream_completion.py — streams partial output tokens from a hosted LLM
(OpenAI gpt-4o-mini).

Uses the OpenAI Chat Completions streaming API (api.openai.com) with the
gpt-4o-mini-2024-07-18 model for token-by-token output.
"""

from __future__ import annotations

import sys
from typing import Iterator, Optional

from model_client import run_stream, run_stream_to_text, resolve_model
from model_models import StreamRequest, StreamChunk, build_stream_request

# Concrete OpenAI model identifier for streaming
STREAM_MODEL = resolve_model("gpt-4o-mini")  # gpt-4o-mini-2024-07-18

STREAM_SYSTEM_PROMPT = (
    "You are a helpful assistant. Respond to the user's prompt in a clear "
    "and engaging manner."
)


def stream_completion(
    prompt: str,
    model: Optional[str] = None,
    temperature: float = 0.7,
    max_tokens: Optional[int] = None,
    system_prompt: Optional[str] = None,
) -> Iterator[StreamChunk]:
    """
    Stream partial tokens from the hosted OpenAI gpt-4o-mini model.

    Parameters
    ----------
    prompt : str
        User prompt.
    model : str, optional
        Concrete OpenAI model ID (defaults to gpt-4o-mini-2024-07-18).
    temperature : float
        Sampling temperature.
    max_tokens : int, optional
        Maximum output tokens.
    system_prompt : str, optional
        Override the default system prompt.

    Yields
    ------
    StreamChunk
        Each chunk containing the next delta of generated text.
    """
    target_model = model or STREAM_MODEL
    sys_prompt = system_prompt or STREAM_SYSTEM_PROMPT
    request = build_stream_request(
        system_prompt=sys_prompt,
        user_prompt=prompt,
        model=target_model,
        temperature=temperature,
        max_tokens=max_tokens,
    )
    yield from run_stream(request)


def stream_completion_to_text(
    prompt: str,
    model: Optional[str] = None,
    temperature: float = 0.7,
    max_tokens: Optional[int] = None,
    system_prompt: Optional[str] = None,
) -> str:
    """
    Stream and accumulate the full response text.

    Returns the complete output as a string.
    """
    target_model = model or STREAM_MODEL
    sys_prompt = system_prompt or STREAM_SYSTEM_PROMPT
    request = build_stream_request(
        system_prompt=sys_prompt,
        user_prompt=prompt,
        model=target_model,
        temperature=temperature,
        max_tokens=max_tokens,
    )
    return run_stream_to_text(request)


def print_stream(
    prompt: str,
    model: Optional[str] = None,
    temperature: float = 0.7,
    max_tokens: Optional[int] = None,
) -> str:
    """Print streamed tokens to stdout in real time and return full text."""
    chunks = stream_completion(prompt, model=model, temperature=temperature, max_tokens=max_tokens)
    accumulated: list[str] = []
    for chunk in chunks:
        if chunk.delta_content:
            accumulated.append(chunk.delta_content)
            sys.stdout.write(chunk.delta_content)
            sys.stdout.flush()
    sys.stdout.write("\n")
    return "".join(accumulated)


if __name__ == "__main__":
    print("Streaming response from OpenAI gpt-4o-mini:\n")
    full_text = print_stream(
        "Explain the concept of recursion in programming in about 100 words."
    )
    print(f"\nTotal length: {len(full_text)} characters")
