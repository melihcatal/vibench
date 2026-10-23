from __future__ import annotations

from typing import Iterable

from model_client import DEFAULT_CHAT_MODEL, build_messages, stream_chat_completion
from model_models import GenerationConfig, StreamCompletionRequest


def stream_completion(
    request: StreamCompletionRequest, model: str = DEFAULT_CHAT_MODEL
) -> Iterable[str]:
    system_prompt = (
        request.system_prompt
        or "You are an OpenAI assistant that streams helpful completions."
    )
    return stream_chat_completion(
        build_messages(system_prompt, request.prompt),
        model=model,
        config=GenerationConfig(temperature=0.4, max_output_tokens=400, top_p=0.95),
    )
