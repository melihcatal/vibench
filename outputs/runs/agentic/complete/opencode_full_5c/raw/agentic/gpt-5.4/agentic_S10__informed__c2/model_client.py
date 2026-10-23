import os
from typing import Generator, Iterable, Optional

from openai import OpenAI

from model_models import (
    GenerationRequest,
    GenerationResult,
    compact_text_parts,
    normalize_text,
    usage_to_dict,
)


DEFAULT_CHAT_MODEL = os.getenv("OPENAI_CHAT_MODEL", "gpt-4.1-mini")
DEFAULT_REASONING_MODEL = os.getenv("OPENAI_REASONING_MODEL", "gpt-4.1")
DEFAULT_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-large")
DEFAULT_TTS_MODEL = os.getenv("OPENAI_TTS_MODEL", "gpt-4o-mini-tts")
DEFAULT_TTS_VOICE = os.getenv("OPENAI_TTS_VOICE", "alloy")


def get_openai_client() -> OpenAI:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is required")
    base_url = os.getenv("OPENAI_BASE_URL")
    if base_url:
        return OpenAI(api_key=api_key, base_url=base_url)
    return OpenAI(api_key=api_key)


def select_chat_model(
    task: str = "default", preferred_model: Optional[str] = None
) -> str:
    if preferred_model:
        return preferred_model
    if task in {"json", "safety_sensitive"}:
        return DEFAULT_REASONING_MODEL
    return DEFAULT_CHAT_MODEL


def build_messages(request: GenerationRequest, task_instruction: str) -> list[dict]:
    system_prompt = compact_text_parts(request.system_prompt, task_instruction)
    user_prompt = compact_text_parts(
        request.prompt,
        request.text,
        f"Context:\n{normalize_text(request.context)}" if request.context else None,
        f"Question:\n{normalize_text(request.question)}" if request.question else None,
    )
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": user_prompt})
    return messages


def create_chat_completion(
    request: GenerationRequest, task_instruction: str
) -> GenerationResult:
    client = get_openai_client()
    model = select_chat_model(task="default", preferred_model=request.model)
    response = client.chat.completions.create(
        model=model,
        messages=build_messages(request, task_instruction),
        temperature=request.temperature,
        top_p=request.top_p,
        max_tokens=request.max_output_tokens,
    )
    choice = response.choices[0]
    content = choice.message.content or ""
    return GenerationResult(
        provider="OpenAI",
        model=response.model,
        text=content,
        usage=usage_to_dict(response.usage),
        finish_reason=choice.finish_reason,
    )


def stream_chat_completion(
    request: GenerationRequest, task_instruction: str
) -> Generator[str, None, None]:
    client = get_openai_client()
    model = select_chat_model(task="default", preferred_model=request.model)
    stream = client.chat.completions.create(
        model=model,
        messages=build_messages(request, task_instruction),
        temperature=request.temperature,
        top_p=request.top_p,
        max_tokens=request.max_output_tokens,
        stream=True,
    )
    for chunk in stream:
        if not chunk.choices:
            continue
        delta = chunk.choices[0].delta
        content = getattr(delta, "content", None)
        if content:
            yield content


def join_stream(chunks: Iterable[str]) -> str:
    return "".join(chunks)
