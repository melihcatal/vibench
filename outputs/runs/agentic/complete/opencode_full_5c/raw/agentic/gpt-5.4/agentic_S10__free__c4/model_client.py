from __future__ import annotations

import os
from typing import Iterable, Iterator, Optional

from openai import OpenAI

from model_models import build_messages


MODEL_FAMILY_DEFAULTS = {
    "summary": "gpt-4.1-mini",
    "extraction": "gpt-4.1-mini",
    "qa": "gpt-4.1-mini",
    "stream": "gpt-4.1-mini",
    "safety": "omni-moderation-latest",
    "translation": "gpt-4.1-mini",
    "embedding": "text-embedding-3-large",
    "speech": "gpt-4o-mini-tts",
}


def get_openai_client() -> OpenAI:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")
    base_url = os.environ.get("OPENAI_BASE_URL")
    if base_url:
        return OpenAI(api_key=api_key, base_url=base_url)
    return OpenAI(api_key=api_key)


def select_model(task_name: str, override: Optional[str] = None) -> str:
    if override:
        return override
    env_key = f"OPENAI_MODEL_{task_name.upper()}"
    return os.environ.get(env_key, MODEL_FAMILY_DEFAULTS[task_name])


def create_text_response(
    system_prompt: str,
    user_prompt: str,
    task_name: str,
    model: Optional[str] = None,
    temperature: float = 0.2,
    max_output_tokens: int = 400,
):
    client = get_openai_client()
    chosen_model = select_model(task_name, model)
    return client.responses.create(
        model=chosen_model,
        input=build_messages(system_prompt, user_prompt),
        temperature=temperature,
        max_output_tokens=max_output_tokens,
    )


def stream_text_response(
    system_prompt: str,
    user_prompt: str,
    model: Optional[str] = None,
    temperature: float = 0.2,
    max_output_tokens: int = 400,
) -> Iterator[str]:
    client = get_openai_client()
    chosen_model = select_model("stream", model)
    with client.responses.stream(
        model=chosen_model,
        input=build_messages(system_prompt, user_prompt),
        temperature=temperature,
        max_output_tokens=max_output_tokens,
    ) as stream:
        for event in stream:
            if getattr(event, "type", "") == "response.output_text.delta":
                delta = getattr(event, "delta", "")
                if delta:
                    yield delta
        stream.until_done()


def collect_stream(chunks: Iterable[str]) -> str:
    return "".join(chunks)
