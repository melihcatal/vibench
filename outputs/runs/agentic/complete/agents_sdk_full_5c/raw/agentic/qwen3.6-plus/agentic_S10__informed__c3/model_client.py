"""
Local configuration and client helper utilities for Hosted LLM Inference
and Model-Family Selection using the Mistral AI platform.

Provider: Mistral AI (mistralai SDK)
Auth: MISTRAL_API_KEY environment variable
"""

from __future__ import annotations

import os
from typing import Any, Dict, Iterator, List, Optional

from mistralai import Mistral
from mistralai.models.chat_completion_response import ChatCompletionResponse
from mistralai.models.chat_completion_stream_event import ChatCompletionStreamEvent

from model_models import (
    LLMRequest,
    LLMResponse,
    StreamedChunk,
    normalize_model_name,
)

MISTRAL_API_HOST = "api.mistral.ai"


def load_mistral_api_key() -> str:
    """Load the Mistral API key from environment variables."""
    api_key = os.environ.get("MISTRAL_API_KEY")
    if not api_key:
        raise ValueError(
            "MISTRAL_API_KEY environment variable is required. "
            "Sign up at https://console.mistral.ai/ to get your API key."
        )
    return api_key


def create_mistral_client(api_key: Optional[str] = None) -> Mistral:
    """Create and return a configured Mistral AI SDK client."""
    key = api_key or load_mistral_api_key()
    client = Mistral(api_key=key)
    return client


def resolve_model(model: Optional[str] = None, model_family: Optional[str] = None) -> str:
    """Resolve a concrete Mistral model identifier from name or family."""
    if model:
        return model
    if model_family:
        return normalize_model_name(model_family)
    from model_models import DEFAULT_MISTRAL_MODEL
    return DEFAULT_MISTRAL_MODEL


def execute_chat(
    request: LLMRequest,
    client: Optional[Mistral] = None,
) -> LLMResponse:
    """Execute a chat completion request against Mistral AI."""
    if client is None:
        client = create_mistral_client()

    payload = request.to_mistral_payload()

    chat_completion: ChatCompletionResponse = client.chat.complete(
        model=payload["model"],
        messages=payload["messages"],
        max_tokens=payload.get("max_tokens"),
        temperature=payload.get("temperature"),
        top_p=payload.get("top_p"),
    )

    return LLMResponse.from_mistral(chat_completion)


def execute_chat_stream(
    request: LLMRequest,
    client: Optional[Mistral] = None,
) -> Iterator[StreamedChunk]:
    """Stream a chat completion request against Mistral AI."""
    if client is None:
        client = create_mistral_client()

    payload = request.to_mistral_payload()
    payload["stream"] = True

    stream = client.chat.stream(
        model=payload["model"],
        messages=payload["messages"],
        max_tokens=payload.get("max_tokens"),
        temperature=payload.get("temperature"),
        top_p=payload.get("top_p"),
    )

    for chunk in stream:
        parsed = StreamedChunk.from_mistral_chunk(chunk)
        if parsed is not None:
            yield parsed


def build_request(
    prompt: str,
    system_prompt: Optional[str] = None,
    model: Optional[str] = None,
    model_family: Optional[str] = None,
    max_tokens: int = 4096,
    temperature: float = 0.7,
    stream: bool = False,
) -> LLMRequest:
    """Factory helper to build an LLMRequest with resolved model."""
    resolved_model = resolve_model(model, model_family)
    return LLMRequest(
        prompt=prompt,
        system_prompt=system_prompt,
        model=resolved_model,
        max_tokens=max_tokens,
        temperature=temperature,
        stream=stream,
    )
