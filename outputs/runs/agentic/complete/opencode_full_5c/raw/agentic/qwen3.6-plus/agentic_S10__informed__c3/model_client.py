import os
from typing import Optional, Iterator
from openai import OpenAI
from model_models import (
    LLMRequest,
    LLMResponse,
    StreamChunk,
    normalize_openai_response,
    normalize_stream_chunk,
    build_messages,
)


def get_openai_client(api_key: Optional[str] = None) -> OpenAI:
    key = api_key or os.environ.get("OPENAI_API_KEY")
    if not key:
        raise ValueError("OPENAI_API_KEY environment variable is required")
    return OpenAI(api_key=key)


def create_chat_completion(
    request: LLMRequest,
    client: Optional[OpenAI] = None,
) -> LLMResponse:
    if client is None:
        client = get_openai_client()

    messages = build_messages(request.system_prompt, request.prompt)

    kwargs = {
        "model": request.model,
        "messages": messages,
        "temperature": request.temperature,
        "max_tokens": request.max_tokens,
    }

    if request.json_mode:
        kwargs["response_format"] = {"type": "json_object"}

    response = client.chat.completions.create(**kwargs)
    return normalize_openai_response(response)


def stream_chat_completion(
    request: LLMRequest,
    client: Optional[OpenAI] = None,
) -> Iterator[StreamChunk]:
    if client is None:
        client = get_openai_client()

    messages = build_messages(request.system_prompt, request.prompt)

    response = client.chat.completions.create(
        model=request.model,
        messages=messages,
        temperature=request.temperature,
        max_tokens=request.max_tokens,
        stream=True,
    )

    for chunk in response:
        normalized = normalize_stream_chunk(chunk)
        if normalized is not None:
            yield normalized
