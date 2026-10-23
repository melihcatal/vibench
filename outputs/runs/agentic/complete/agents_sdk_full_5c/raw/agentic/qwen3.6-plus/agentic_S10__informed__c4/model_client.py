"""
Local configuration and client helper utilities for Hosted LLM Inference
and Model-Family Selection using Anthropic Messages API.
"""

import os
from typing import Optional, Dict, Any, List

import anthropic


ANTHROPIC_MODEL_FAMILY = "claude"
DEFAULT_MODEL_ID = "claude-3-5-sonnet-20241022"


def get_anthropic_client() -> anthropic.Anthropic:
    """Create and return an authenticated Anthropic client."""
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable is required")
    return anthropic.Anthropic(api_key=api_key)


def build_messages_prompt(
    system_prompt: Optional[str] = None,
    user_prompt: Optional[str] = None,
    messages: Optional[List[Dict[str, str]]] = None,
) -> List[Dict[str, str]]:
    """Build a messages list for Anthropic API requests."""
    result: List[Dict[str, str]] = []
    if messages:
        result.extend(messages)
    elif user_prompt:
        result.append({"role": "user", "content": user_prompt})
    return result


def normalize_completion_response(
    response: anthropic.types.Message,
) -> Dict[str, Any]:
    """Normalize an Anthropic Message response into a standard dict."""
    content_text = ""
    for block in response.content:
        if block.type == "text":
            content_text += block.text
    return {
        "text": content_text,
        "model": response.model,
        "stop_reason": response.stop_reason,
        "usage": {
            "input_tokens": response.usage.input_tokens,
            "output_tokens": response.usage.output_tokens,
        },
        "id": response.id,
    }


def prepare_api_request(
    model_id: str = DEFAULT_MODEL_ID,
    max_tokens: int = 4096,
    temperature: float = 0.7,
    system_prompt: Optional[str] = None,
    messages: Optional[List[Dict[str, str]]] = None,
    user_prompt: Optional[str] = None,
) -> Dict[str, Any]:
    """Prepare a request dictionary for the Anthropic Messages API."""
    request: Dict[str, Any] = {
        "model": model_id,
        "max_tokens": max_tokens,
        "temperature": temperature,
        "messages": build_messages_prompt(system_prompt, user_prompt, messages),
    }
    if system_prompt:
        request["system"] = system_prompt
    return request
