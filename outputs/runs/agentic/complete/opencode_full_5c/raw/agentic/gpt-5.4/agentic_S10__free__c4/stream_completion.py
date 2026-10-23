from __future__ import annotations

from model_client import collect_stream, stream_text_response


def stream_completion(prompt: str, model: str | None = None):
    return stream_text_response(
        system_prompt="You are a helpful assistant that completes prompts in a fluent and faithful way.",
        user_prompt=prompt,
        model=model,
        temperature=0.4,
        max_output_tokens=300,
    )


def collect_completion(prompt: str, model: str | None = None) -> dict:
    chunks = list(stream_completion(prompt, model=model))
    return {
        "text": collect_stream(chunks),
        "chunks": chunks,
        "model": model or "gpt-4.1-mini",
    }
