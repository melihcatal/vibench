import os
from typing import Optional

from openai import OpenAI

from model_models import (
    LLMRequest,
    LLMResponse,
    StreamChunk,
    normalize_openai_response,
    normalize_stream_chunk,
)


def get_openai_api_key() -> str:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is not set")
    return api_key


def create_openai_client(api_key: Optional[str] = None) -> OpenAI:
    key = api_key or get_openai_api_key()
    return OpenAI(api_key=key)


def execute_llm_request(
    request: LLMRequest,
    client: Optional[OpenAI] = None,
    api_key: Optional[str] = None,
) -> LLMResponse:
    if client is None:
        client = create_openai_client(api_key)
    kwargs = request.to_openai_kwargs()
    response = client.chat.completions.create(**kwargs)
    return normalize_openai_response(response)


def execute_streaming_request(
    request: LLMRequest,
    client: Optional[OpenAI] = None,
    api_key: Optional[str] = None,
):
    if client is None:
        client = create_openai_client(api_key)
    stream_request = LLMRequest(
        model=request.model,
        messages=request.messages if request.messages else None,
        system_prompt=request.system_prompt,
        user_prompt=request.user_prompt,
        temperature=request.temperature,
        max_tokens=request.max_tokens,
        top_p=request.top_p,
        stream=True,
        json_mode=request.json_mode,
        stop_sequences=request.stop_sequences,
    )
    kwargs = stream_request.to_openai_kwargs()
    stream = client.chat.completions.create(**kwargs)
    for chunk in stream:
        yield normalize_stream_chunk(chunk)


def collect_streamed_text(chunks) -> str:
    parts = []
    for chunk in chunks:
        if chunk.delta:
            parts.append(chunk.delta)
    return "".join(parts)


def get_model_family(model_id: str) -> str:
    model_families = {
        "gpt-4o": "gpt-4o",
        "gpt-4o-mini": "gpt-4o-mini",
        "gpt-4-turbo": "gpt-4",
        "gpt-4": "gpt-4",
        "gpt-3.5-turbo": "gpt-3.5",
        "o1": "o1",
        "o1-mini": "o1-mini",
        "o3-mini": "o3-mini",
    }
    for prefix, family in model_families.items():
        if model_id.startswith(prefix):
            return family
    return "unknown"


def select_model_for_task(
    task_type: str,
    require_json: bool = False,
    require_streaming: bool = False,
    prefer_fast: bool = False,
) -> str:
    if require_json and not require_streaming:
        return "gpt-4o"
    if require_streaming and prefer_fast:
        return "gpt-4o-mini"
    if require_streaming:
        return "gpt-4o"
    if task_type in ("summarization", "qa", "extraction"):
        return "gpt-4o"
    if prefer_fast:
        return "gpt-4o-mini"
    return "gpt-4o"
