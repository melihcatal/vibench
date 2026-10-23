import os
from typing import Optional, Iterator

from openai import OpenAI

from model_models import (
    ModelRequest,
    ModelResponse,
    StreamChunk,
    parse_openai_response,
    parse_openai_stream_chunk,
    build_messages,
)

DEFAULT_MODEL = "gpt-4o"
OPENAI_API_BASE = "https://api.openai.com/v1"


def get_openai_client() -> OpenAI:
    api_key = os.environ.get("OPENAI_API_KEY", "")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")
    return OpenAI(api_key=api_key, base_url=OPENAI_API_BASE)


def create_chat_completion(
    request: ModelRequest,
    client: Optional[OpenAI] = None,
    default_system: str = "",
) -> ModelResponse:
    if client is None:
        client = get_openai_client()

    messages = build_messages(request, default_system)

    params = {
        "model": request.model or DEFAULT_MODEL,
        "messages": messages,
        "temperature": request.temperature,
        "max_tokens": request.max_tokens,
        "top_p": request.top_p,
        "frequency_penalty": request.frequency_penalty,
        "presence_penalty": request.presence_penalty,
    }

    if request.json_mode:
        params["response_format"] = {"type": "json_object"}

    if request.stop_sequences:
        params["stop"] = request.stop_sequences

    response = client.chat.completions.create(**params)
    return parse_openai_response(response)


def stream_chat_completion(
    request: ModelRequest,
    client: Optional[OpenAI] = None,
    default_system: str = "",
) -> Iterator[StreamChunk]:
    if client is None:
        client = get_openai_client()

    messages = build_messages(request, default_system)

    params = {
        "model": request.model or DEFAULT_MODEL,
        "messages": messages,
        "temperature": request.temperature,
        "max_tokens": request.max_tokens,
        "stream": True,
    }

    if request.json_mode:
        params["response_format"] = {"type": "json_object"}

    stream = client.chat.completions.create(**params)

    for chunk in stream:
        parsed = parse_openai_stream_chunk(chunk)
        if parsed is not None:
            yield parsed


def create_embedding(
    texts: list[str],
    model: str = "text-embedding-3-small",
    client: Optional[OpenAI] = None,
) -> list[list[float]]:
    if client is None:
        client = get_openai_client()

    response = client.embeddings.create(
        model=model,
        input=texts,
    )

    sorted_data = sorted(response.data, key=lambda x: x.index)
    return [item.embedding for item in sorted_data]
