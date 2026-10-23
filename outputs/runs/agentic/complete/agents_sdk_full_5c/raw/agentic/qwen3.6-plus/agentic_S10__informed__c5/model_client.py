"""
Local helper: Provide local configuration and client helper utilities
for Hosted LLM Inference and Model-Family Selection.

Provider: OpenAI / GPT via OpenAI API
SDK: openai
Auth: OPENAI_API_KEY
"""

import os
from typing import Optional, Dict, Any, List

from openai import OpenAI, AsyncOpenAI


def get_openai_api_key() -> str:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError(
            "OPENAI_API_KEY environment variable is required for OpenAI client."
        )
    return api_key


def create_openai_client(
    api_key: Optional[str] = None,
    organization: Optional[str] = None,
    project: Optional[str] = None,
    base_url: Optional[str] = None,
) -> OpenAI:
    """
    Create a synchronous OpenAI client for chat completions and embeddings.

    Uses the OPENAI_API_KEY environment variable by default.
    """
    return OpenAI(
        api_key=api_key or get_openai_api_key(),
        organization=organization,
        project=project,
        base_url=base_url,
    )


def create_async_openai_client(
    api_key: Optional[str] = None,
    organization: Optional[str] = None,
    project: Optional[str] = None,
    base_url: Optional[str] = None,
) -> AsyncOpenAI:
    """
    Create an asynchronous OpenAI client for streaming completions.
    """
    return AsyncOpenAI(
        api_key=api_key or get_openai_api_key(),
        organization=organization,
        project=project,
        base_url=base_url,
    )


def build_system_message(content: str) -> Dict[str, str]:
    """Build a system role message dict."""
    return {"role": "system", "content": content}


def build_user_message(content: str) -> Dict[str, str]:
    """Build a user role message dict."""
    return {"role": "user", "content": content}


def build_messages(
    system_prompt: Optional[str] = None,
    user_prompt: Optional[str] = None,
    extra_messages: Optional[List[Dict[str, str]]] = None,
) -> List[Dict[str, str]]:
    """
    Assemble a list of messages for OpenAI chat completions.
    """
    messages: List[Dict[str, str]] = []
    if system_prompt:
        messages.append(build_system_message(system_prompt))
    if user_prompt:
        messages.append(build_user_message(user_prompt))
    if extra_messages:
        messages.extend(extra_messages)
    return messages


def get_default_model() -> str:
    """Return the default OpenAI model identifier."""
    return "gpt-4o"


def get_fast_model() -> str:
    """Return a faster, smaller OpenAI model for simpler tasks."""
    return "gpt-4o-mini"


def normalize_openai_response(response: Any) -> str:
    """
    Extract the assistant message content from an OpenAI chat completion response.
    """
    if response and response.choices:
        choice = response.choices[0]
        if choice.message and choice.message.content:
            return choice.message.content.strip()
    return ""


def normalize_stream_delta(delta: Any) -> Optional[str]:
    """
    Extract content from a streaming chunk delta.
    Returns None if no content is present.
    """
    if delta and hasattr(delta, "content") and delta.content is not None:
        return delta.content
    return None
