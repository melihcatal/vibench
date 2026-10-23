"""
stream_completion.py - Streams partial output tokens from a hosted OpenAI LLM.

Uses the OpenAI Chat Completions API streaming endpoint for incremental token generation.
"""

from typing import Generator, Optional

from openai import Stream
from openai.types.chat import ChatCompletionChunk

from model_client import get_openai_client, select_model, build_chat_messages, extract_stream_text
from model_models import LLMRequest, StreamChunk


def stream_completion(
    system_prompt: str,
    user_content: str,
    model_family: str = "gpt-4o",
    temperature: float = 0.7,
    max_tokens: int = 1024,
) -> Generator[StreamChunk, None, None]:
    """
    Stream partial output tokens from OpenAI's hosted LLM.

    Yields StreamChunk objects as tokens are generated, allowing
    real-time processing of the response.

    Args:
        system_prompt: The system instruction for the model.
        user_content: The user's input content.
        model_family: OpenAI model family (e.g. "gpt-4o").
        temperature: Sampling temperature.
        max_tokens: Maximum tokens to generate.

    Yields:
        StreamChunk objects with text deltas as they arrive.
    """
    client = get_openai_client()
    model_id = select_model(model_family)

    messages = build_chat_messages(
        system_prompt=system_prompt,
        user_content=user_content,
    )

    stream: Stream[ChatCompletionChunk] = client.chat.completions.create(
        model=model_id,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
        stream=True,
    )

    for chunk in stream:
        delta_text = extract_stream_text(chunk)
        if delta_text is not None:
            yield StreamChunk(
                text_delta=delta_text,
                is_last=False,
                model_used=model_id,
                raw_chunk=chunk,
            )

    # Signal end of stream
    yield StreamChunk(
        text_delta="",
        is_last=True,
        model_used=model_id,
    )


def collect_streamed_output(
    system_prompt: str,
    user_content: str,
    model_family: str = "gpt-4o",
    temperature: float = 0.7,
    max_tokens: int = 1024,
    on_chunk: Optional[callable] = None,
) -> str:
    """
    Stream tokens and collect them into a complete string.

    Args:
        system_prompt: The system instruction.
        user_content: The user input.
        model_family: OpenAI model family.
        temperature: Sampling temperature.
        max_tokens: Maximum tokens.
        on_chunk: Optional callback invoked for each chunk.

    Returns:
        The fully assembled text response.
    """
    collected_chunks: list[StreamChunk] = []

    for chunk in stream_completion(
        system_prompt, user_content, model_family, temperature, max_tokens
    ):
        collected_chunks.append(chunk)
        if on_chunk and not chunk.is_last:
            on_chunk(chunk.text_delta, chunk)

    final_text = "".join(
        c.text_delta for c in collected_chunks if c.text_delta
    )
    return final_text


def stream_summarization(
    text: str,
    max_words: int = 150,
    model_family: str = "gpt-4o",
) -> str:
    """
    Stream a summary of the provided text token by token.

    Args:
        text: The text to summarize.
        max_words: Target max words in summary.
        model_family: OpenAI model family.

    Returns:
        The complete summary string.
    """
    system_prompt = (
        "You are an expert summarizer powered by OpenAI. "
        "Provide a concise summary of the provided text."
    )
    user_content = f"Summarize the following text in about {max_words} words:\n\n{text}"

    return collect_streamed_output(
        system_prompt=system_prompt,
        user_content=user_content,
        model_family=model_family,
        temperature=0.3,
        max_tokens=512,
    )


if __name__ == "__main__":
    import sys

    print("Streaming response from OpenAI gpt-4o:\n")
    full_text = ""

    for chunk in stream_completion(
        system_prompt="You are a helpful AI assistant powered by OpenAI.",
        user_content="Write a short 3-sentence explanation of how large language models work.",
        model_family="gpt-4o",
        temperature=0.7,
        max_tokens=256,
    ):
        if not chunk.is_last:
            sys.stdout.write(chunk.text_delta)
            sys.stdout.flush()
            full_text += chunk.text_delta

    print(f"\n\nFull response length: {len(full_text)} characters")
