"""
Provide local configuration and client helper utilities for Hosted LLM Inference
and Model-Family Selection.
"""

import os
from typing import Any, Dict, Iterator, Optional

from openai import OpenAI
from openai.types.chat import ChatCompletion, ChatCompletionChunk

from model_models import (
    LLMRequest,
    LLMResponse,
    StreamChunk,
    normalize_openai_chunk,
    normalize_openai_response,
)


_OPENAI_BASE_URL = "https://api.openai.com/v1"
_DEFAULT_MODEL = "gpt-4o"
_DEFAULT_TEMPERATURE = 0.7
_DEFAULT_MAX_TOKENS = 1024


def get_openai_api_key() -> str:
    """Retrieve OpenAI API key from environment."""
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError(
            "OPENAI_API_KEY environment variable is required. "
            "Set it with your OpenAI platform API key."
        )
    return api_key


def create_openai_client(api_key: Optional[str] = None) -> OpenAI:
    """Create an OpenAI client instance configured for api.openai.com."""
    key = api_key or get_openai_api_key()
    return OpenAI(
        api_key=key,
        base_url=_OPENAI_BASE_URL,
    )


def build_chat_payload(request: LLMRequest) -> Dict[str, Any]:
    """Build an OpenAI chat completions payload from a normalized request."""
    messages = []
    if request.system_prompt:
        messages.append({"role": "system", "content": request.system_prompt})
    messages.append({"role": "user", "content": request.prompt})

    payload: Dict[str, Any] = {
        "model": request.model,
        "messages": messages,
        "temperature": request.temperature,
        "max_tokens": request.max_tokens,
        "top_p": request.top_p,
        "frequency_penalty": request.frequency_penalty,
        "presence_penalty": request.presence_penalty,
        "stream": request.stream,
    }

    if request.stop_sequences:
        payload["stop"] = request.stop_sequences
    if request.response_format:
        payload["response_format"] = request.response_format

    return payload


def execute_chat_completion(
    request: LLMRequest, client: Optional[OpenAI] = None
) -> LLMResponse:
    """Execute a synchronous chat completion and return normalized response."""
    if client is None:
        client = create_openai_client()

    payload = build_chat_payload(request)
    response: ChatCompletion = client.chat.completions.create(**payload)
    return normalize_openai_response(response)


def execute_stream_completion(
    request: LLMRequest, client: Optional[OpenAI] = None
) -> Iterator[StreamChunk]:
    """Execute a streaming chat completion and yield normalized chunks."""
    if client is None:
        client = create_openai_client()

    payload = build_chat_payload(request)
    payload["stream"] = True

    stream = client.chat.completions.create(**payload)
    for chunk in stream:
        normalized = normalize_openai_chunk(chunk)
        yield normalized


def select_model_for_task(
    task_type: str,
    latency_preference: str = "balanced",
    quality_preference: str = "high",
) -> str:
    """Select an appropriate OpenAI model based on task requirements.

    Args:
        task_type: Type of task (summarize, extract, answer, stream, etc.)
        latency_preference: 'low', 'balanced', or 'high'
        quality_preference: 'low', 'balanced', or 'high'

    Returns:
        Concrete OpenAI model identifier string.
    """
    if quality_preference == "high" and task_type in ("extract", "answer"):
        return "gpt-4o"
    elif latency_preference == "low":
        return "gpt-4o-mini"
    elif task_type == "summarize":
        return "gpt-4o"
    elif task_type == "stream":
        return "gpt-4o-mini"
    else:
        return _DEFAULT_MODEL


def validate_model_availability(model_id: str, client: Optional[OpenAI] = None) -> bool:
    """Check if a model is available on the OpenAI platform."""
    if client is None:
        client = create_openai_client()

    known_models = {
        "gpt-4o",
        "gpt-4o-mini",
        "gpt-4-turbo",
        "gpt-3.5-turbo",
        "text-embedding-3-small",
        "text-embedding-3-large",
        "text-moderation-latest",
        "whisper-1",
    }
    return model_id in known_models
