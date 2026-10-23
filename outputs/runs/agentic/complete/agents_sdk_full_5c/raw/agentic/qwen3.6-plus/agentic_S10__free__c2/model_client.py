"""
Local configuration and client helper utilities for Hosted LLM Inference and Model-Family Selection.
Provider: OpenAI - https://platform.openai.com
"""

import os
from openai import OpenAI, AsyncOpenAI
from typing import Optional, Dict, Any


OPENAI_API_BASE = "https://api.openai.com/v1"
OPENAI_DEFAULT_TIMEOUT = 60.0
OPENAI_MAX_RETRIES = 3

MODEL_FAMILIES = {
    "gpt-4o": "openai-gpt4o",
    "gpt-4o-mini": "openai-gpt4o-mini",
    "gpt-4-turbo": "openai-gpt4-turbo",
    "gpt-3.5-turbo": "openai-gpt35-turbo",
    "text-embedding-3-small": "openai-embedding-small",
    "text-embedding-3-large": "openai-embedding-large",
    "tts-1": "openai-tts",
    "tts-1-hd": "openai-tts-hd",
}

DEFAULT_SUMMARIZE_MODEL = "gpt-4o"
DEFAULT_EXTRACT_MODEL = "gpt-4o"
DEFAULT_QA_MODEL = "gpt-4o"
DEFAULT_STREAM_MODEL = "gpt-3.5-turbo"
DEFAULT_EMBEDDING_MODEL = "text-embedding-3-small"
DEFAULT_TTS_MODEL = "tts-1"


def _resolve_api_key() -> str:
    api_key = os.environ.get("OPENAI_API_KEY")
    if api_key is None:
        raise ValueError(
            "OPENAI_API_KEY environment variable is required for OpenAI provider integration"
        )
    return api_key


def _resolve_base_url() -> str:
    return os.environ.get("OPENAI_BASE_URL", OPENAI_API_BASE)


def get_openai_client(
    api_key: Optional[str] = None,
    base_url: Optional[str] = None,
    timeout: Optional[float] = None,
    max_retries: Optional[int] = None,
    organization: Optional[str] = None,
) -> OpenAI:
    """Create a synchronous OpenAI client with resolved configuration."""
    key = api_key or _resolve_api_key()
    url = base_url or _resolve_base_url()
    t = timeout if timeout is not None else OPENAI_DEFAULT_TIMEOUT
    retries = max_retries if max_retries is not None else OPENAI_MAX_RETRIES
    org = organization or os.environ.get("OPENAI_ORG_ID")

    client_kwargs: Dict[str, Any] = {
        "api_key": key,
        "base_url": url,
        "timeout": t,
        "max_retries": retries,
    }
    if org:
        client_kwargs["organization"] = org

    return OpenAI(**client_kwargs)


def get_async_openai_client(
    api_key: Optional[str] = None,
    base_url: Optional[str] = None,
    timeout: Optional[float] = None,
    max_retries: Optional[int] = None,
    organization: Optional[str] = None,
) -> AsyncOpenAI:
    """Create an asynchronous OpenAI client with resolved configuration."""
    key = api_key or _resolve_api_key()
    url = base_url or _resolve_base_url()
    t = timeout if timeout is not None else OPENAI_DEFAULT_TIMEOUT
    retries = max_retries if max_retries is not None else OPENAI_MAX_RETRIES
    org = organization or os.environ.get("OPENAI_ORG_ID")

    client_kwargs: Dict[str, Any] = {
        "api_key": key,
        "base_url": url,
        "timeout": t,
        "max_retries": retries,
    }
    if org:
        client_kwargs["organization"] = org

    return AsyncOpenAI(**client_kwargs)


def resolve_model_family(model_name: str) -> str:
    """Map a concrete OpenAI model identifier to its model family string."""
    return MODEL_FAMILIES.get(model_name, "openai-unknown")


def build_system_prompt(instructions: str) -> str:
    """Build a system prompt string for OpenAI chat completions."""
    return instructions


def extract_first_text(content: Any) -> str:
    """Extract the first text block from OpenAI chat completion content."""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        for part in content:
            if isinstance(part, dict) and part.get("type") == "text":
                return part["text"]
            if hasattr(part, "text"):
                return part.text
    if hasattr(content, "__iter__"):
        try:
            return next(iter(content)).text
        except (StopIteration, AttributeError):
            pass
    return str(content) if content is not None else ""
