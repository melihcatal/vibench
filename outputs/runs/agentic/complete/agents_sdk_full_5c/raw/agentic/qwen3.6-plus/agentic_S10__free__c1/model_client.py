"""
Local configuration and client helper utilities for Hosted LLM Inference
and Model-Family Selection.

Provides OpenAI client initialization, environment-variable loading, and
convenience wrapper functions for common completion patterns.
"""

from __future__ import annotations

import os
from typing import Any, Dict, Iterator, Optional

import openai

from model_models import (
    OPENAI_MODEL_FAMILIES,
    DEFAULT_CHAT_MODEL,
    CompletionRequest,
    CompletionResponse,
    StreamRequest,
    StreamChunk,
    ModerationRequest,
    ModerationResponse,
    EmbeddingRequest,
    EmbeddingResponse,
    SpeechRequest,
    collect_stream_chunks,
    parse_json_response,
)


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

OPENAI_API_KEY_ENV = "OPENAI_API_KEY"
OPENAI_BASE_URL_ENV = "OPENAI_BASE_URL"


def get_api_key() -> str:
    key = os.environ.get(OPENAI_API_KEY_ENV)
    if not key:
        raise EnvironmentError(
            f"Environment variable {OPENAI_API_KEY_ENV} is not set. "
            "Please set your OpenAI API key before running."
        )
    return key


def get_base_url() -> Optional[str]:
    return os.environ.get(OPENAI_BASE_URL_ENV)


# ---------------------------------------------------------------------------
# Client factory
# ---------------------------------------------------------------------------

_openai_client: Optional[openai.OpenAI] = None


def get_openai_client() -> openai.OpenAI:
    """Return a singleton OpenAI SDK client configured from environment."""
    global _openai_client
    if _openai_client is None:
        kwargs: Dict[str, Any] = {"api_key": get_api_key()}
        base_url = get_base_url()
        if base_url:
            kwargs["base_url"] = base_url
        _openai_client = openai.OpenAI(**kwargs)
    return _openai_client


def reset_client() -> None:
    """Reset the singleton client (useful for testing)."""
    global _openai_client
    _openai_client = None


# ---------------------------------------------------------------------------
# Core completion helpers
# ---------------------------------------------------------------------------

def run_completion(
    request: CompletionRequest,
    client: Optional[openai.OpenAI] = None,
) -> CompletionResponse:
    """Execute a non-streaming chat completion against OpenAI."""
    cl = client or get_openai_client()
    payload = request.to_openai_payload()
    response = cl.chat.completions.create(**payload)
    return CompletionResponse.from_openai(response)


def run_stream(
    request: StreamRequest,
    client: Optional[openai.OpenAI] = None,
) -> Iterator[StreamChunk]:
    """Yield streamed chunks from OpenAI chat completion."""
    cl = client or get_openai_client()
    payload = request.to_openai_payload()
    stream = cl.chat.completions.create(**payload)
    for chunk in stream:
        yield StreamChunk.from_openai_chunk(chunk)


def run_stream_to_text(
    request: StreamRequest,
    client: Optional[openai.OpenAI] = None,
) -> str:
    """Run a streaming request and return the fully accumulated text."""
    chunks = run_stream(request, client=client)
    return collect_stream_chunks(chunks)


# ---------------------------------------------------------------------------
# Moderation helper
# ---------------------------------------------------------------------------

def check_moderation(
    request: ModerationRequest,
    client: Optional[openai.OpenAI] = None,
) -> ModerationResponse:
    """Check text against the OpenAI moderation endpoint."""
    cl = client or get_openai_client()
    payload = request.to_openai_payload()
    response = cl.moderations.create(**payload)
    return ModerationResponse.from_openai(response)


# ---------------------------------------------------------------------------
# Embedding helper
# ---------------------------------------------------------------------------

def generate_embeddings(
    request: EmbeddingRequest,
    client: Optional[openai.OpenAI] = None,
) -> EmbeddingResponse:
    """Generate embeddings via the OpenAI embeddings API."""
    cl = client or get_openai_client()
    payload = request.to_openai_payload()
    response = cl.embeddings.create(**payload)
    return EmbeddingResponse.from_openai(response)


# ---------------------------------------------------------------------------
# Speech (TTS) helper
# ---------------------------------------------------------------------------

def generate_speech(
    request: SpeechRequest,
    client: Optional[openai.OpenAI] = None,
) -> bytes:
    """Generate audio from text via the OpenAI speech endpoint."""
    cl = client or get_openai_client()
    payload = request.to_openai_payload()
    response = cl.audio.speech.create(**payload)
    return response.content


# ---------------------------------------------------------------------------
# Convenience: resolve model family by name
# ---------------------------------------------------------------------------

def resolve_model(family_name: str) -> str:
    """Map a friendly family name to the concrete OpenAI model ID."""
    model = OPENAI_MODEL_FAMILIES.get(family_name)
    if model is None:
        raise ValueError(
            f"Unknown model family '{family_name}'. "
            f"Available: {list(OPENAI_MODEL_FAMILIES.keys())}"
        )
    return model
