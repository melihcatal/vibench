from __future__ import annotations

from typing import Generator, List, Optional

from model_client import create_stream_completion
from model_models import LLMRequest, StreamChunk, normalize_messages


def stream_completion(
    prompt: str,
    system_prompt: Optional[str] = None,
    history: Optional[List[Dict[str, str]]] = None,
    model: str = "gpt-4o-2024-08-06",
    temperature: float = 0.7,
    max_tokens: Optional[int] = None,
) -> Generator[str, None, None]:
    messages = normalize_messages(
        system_prompt=system_prompt,
        user_prompt=prompt,
        history=history,
    )

    request = LLMRequest(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
        stream=True,
    )

    for chunk in create_stream_completion(request):
        if chunk.delta:
            yield chunk.delta


def stream_completion_collected(
    prompt: str,
    system_prompt: Optional[str] = None,
    history: Optional[List[Dict[str, str]]] = None,
    model: str = "gpt-4o-2024-08-06",
    temperature: float = 0.7,
    max_tokens: Optional[int] = None,
) -> str:
    collected: List[str] = []
    for token in stream_completion(
        prompt=prompt,
        system_prompt=system_prompt,
        history=history,
        model=model,
        temperature=temperature,
        max_tokens=max_tokens,
    ):
        collected.append(token)
    return "".join(collected)


if __name__ == "__main__":
    import sys

    input_prompt = sys.stdin.read()
    for token in stream_completion(input_prompt):
        print(token, end="", flush=True)
    print()
