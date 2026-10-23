"""
Local configuration and client helper utilities for Hosted LLM Inference
and Model-Family Selection using the OpenAI Chat Completions API.

Provider: OpenAI / Azure OpenAI chat completions
SDK: openai
Auth: OPENAI_API_KEY
Concrete model identifiers used: gpt-4o, gpt-4o-mini
"""

import os
from typing import Any, Dict, Iterator, Optional

from openai import OpenAI

from model_models import (
    LLMRequest,
    LLMResponse,
    UsageInfo,
    normalize_openai_completion,
    normalize_openai_stream_delta,
)


def _resolve_openai_config() -> Dict[str, Any]:
    """Resolve OpenAI configuration from environment variables."""
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise EnvironmentError(
            "OPENAI_API_KEY is required for OpenAI Chat Completions integration"
        )
    base_url = os.environ.get("OPENAI_BASE_URL")
    config: Dict[str, Any] = {"api_key": api_key}
    if base_url:
        config["base_url"] = base_url
    return config


def create_openai_client() -> OpenAI:
    """Create and return a configured OpenAI client instance."""
    config = _resolve_openai_config()
    return OpenAI(**config)


def build_payload(request: LLMRequest) -> Dict[str, Any]:
    """
    Build an OpenAI Chat Completions API payload from an LLMRequest.
    Uses concrete OpenAI model identifiers like 'gpt-4o' or 'gpt-4o-mini'.
    """
    messages = [{"role": "system", "content": request.system_prompt}]
    messages.append({"role": "user", "content": request.user_prompt})

    payload: Dict[str, Any] = {
        "model": request.model_name or "gpt-4o",
        "messages": messages,
        "temperature": request.temperature or 0.7,
        "max_tokens": request.max_tokens or 2048,
    }

    if request.json_mode:
        payload["response_format"] = {"type": "json_object"}

    return payload


def call_llm_sync(request: LLMRequest) -> LLMResponse:
    """
    Synchronously call the OpenAI Chat Completions API.

    Provider: OpenAI
    Model family: gpt-4o (default) or specified via request.model_name
    Endpoint: api.openai.com/v1/chat/completions
    """
    client = create_openai_client()
    payload = build_payload(request)

    completion = client.chat.completions.create(**payload)
    return normalize_openai_completion(completion)


def call_llm_stream(request: LLMRequest) -> Iterator[str]:
    """
    Stream partial output tokens from the OpenAI Chat Completions API.

    Provider: OpenAI
    Model family: gpt-4o (default) or specified via request.model_name
    Endpoint: api.openai.com/v1/chat/completions
    """
    client = create_openai_client()
    payload = build_payload(request)
    payload["stream"] = True

    stream = client.chat.completions.create(**payload)
    for chunk in stream:
        delta_text = normalize_openai_stream_delta(chunk)
        if delta_text:
            yield delta_text
