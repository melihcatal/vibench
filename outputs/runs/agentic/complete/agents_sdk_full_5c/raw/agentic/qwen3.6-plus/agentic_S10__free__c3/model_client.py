"""
Local configuration and client helper utilities for Hosted LLM Inference
and Model-Family Selection using the OpenAI platform.
"""

import os
from typing import Optional, Dict, Any, List

from openai import OpenAI, AsyncOpenAI
from openai.types.chat import ChatCompletionMessageParam


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")

DEFAULT_SUMMARIZE_MODEL = "gpt-4o-2024-08-06"
DEFAULT_EXTRACTION_MODEL = "gpt-4o-2024-08-06"
DEFAULT_QA_MODEL = "gpt-4o-2024-08-06"
DEFAULT_STREAM_MODEL = "gpt-4o-2024-08-06"
DEFAULT_MODERATION_MODEL = "omni-moderation-latest"
DEFAULT_TRANSLATION_MODEL = "gpt-4o-2024-08-06"
DEFAULT_EMBEDDING_MODEL = "text-embedding-3-small"
DEFAULT_TTS_MODEL = "tts-1"

MODEL_FAMILY_GPT4O = "gpt-4o"
MODEL_FAMILY_GPT4O_MINI = "gpt-4o-mini"
MODEL_FAMILY_GPT35 = "gpt-3.5-turbo"


def get_sync_client(api_key: Optional[str] = None, base_url: Optional[str] = None) -> OpenAI:
    """Return a synchronous OpenAI client configured for api.openai.com."""
    key = api_key or OPENAI_API_KEY
    url = base_url or OPENAI_BASE_URL
    return OpenAI(api_key=key, base_url=url)


def get_async_client(api_key: Optional[str] = None, base_url: Optional[str] = None) -> AsyncOpenAI:
    """Return an asynchronous OpenAI client configured for api.openai.com."""
    key = api_key or OPENAI_API_KEY
    url = base_url or OPENAI_BASE_URL
    return AsyncOpenAI(api_key=key, base_url=url)


def build_system_message(instruction: str) -> ChatCompletionMessageParam:
    """Build a system message dict for OpenAI chat completions."""
    return {"role": "system", "content": instruction}


def build_user_message(content: str) -> ChatCompletionMessageParam:
    """Build a user message dict for OpenAI chat completions."""
    return {"role": "user", "content": content}


def build_assistant_message(content: str) -> ChatCompletionMessageParam:
    """Build an assistant message dict for OpenAI chat completions."""
    return {"role": "assistant", "content": content}


def select_model_family(task: str, latency_budget: str = "normal") -> str:
    """
    Select an OpenAI model family based on the task and latency requirements.

    Args:
        task: One of 'summarize', 'extract', 'qa', 'stream', 'moderation', 'translate', 'embed', 'tts'.
        latency_budget: 'low', 'normal', or 'high' (lower latency = smaller model).

    Returns:
        The concrete OpenAI model identifier.
    """
    if latency_budget == "low":
        return MODEL_FAMILY_GPT4O_MINI + "-2024-07-18"
    if latency_budget == "high":
        return DEFAULT_SUMMARIZE_MODEL

    if task == "summarize":
        return DEFAULT_SUMMARIZE_MODEL
    if task == "extract":
        return DEFAULT_EXTRACTION_MODEL
    if task == "qa":
        return DEFAULT_QA_MODEL
    if task == "stream":
        return DEFAULT_STREAM_MODEL
    if task == "moderation":
        return DEFAULT_MODERATION_MODEL
    if task == "translate":
        return DEFAULT_TRANSLATION_MODEL
    if task == "embed":
        return DEFAULT_EMBEDDING_MODEL
    if task == "tts":
        return DEFAULT_TTS_MODEL

    return DEFAULT_SUMMARIZE_MODEL


def configure_completion_kwargs(
    messages: List[ChatCompletionMessageParam],
    model: str,
    temperature: float = 0.7,
    max_tokens: int = 4096,
    response_format: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Build kwargs for an OpenAI chat.completions.create call.

    Args:
        messages: List of message dicts.
        model: OpenAI model identifier (e.g., gpt-4o-2024-08-06).
        temperature: Sampling temperature.
        max_tokens: Maximum tokens to generate.
        response_format: Optional dict for response_format parameter (e.g., {"type": "json_object"}).

    Returns:
        Dict of kwargs suitable for client.chat.completions.create().
    """
    kwargs: Dict[str, Any] = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
    }
    if response_format is not None:
        kwargs["response_format"] = response_format
    return kwargs
