import os
from typing import Optional, Dict, Any
from openai import OpenAI, AsyncOpenAI


DEFAULT_MODEL = "gpt-4o"
DEFAULT_TEMPERATURE = 0.7
DEFAULT_MAX_TOKENS = 4096
OPENAI_API_BASE = "https://api.openai.com/v1"


def get_openai_api_key() -> str:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")
    return api_key


def get_openai_organization() -> Optional[str]:
    return os.environ.get("OPENAI_ORGANIZATION")


def get_openai_project() -> Optional[str]:
    return os.environ.get("OPENAI_PROJECT")


def create_openai_client(
    api_key: Optional[str] = None,
    organization: Optional[str] = None,
    project: Optional[str] = None,
    base_url: Optional[str] = None,
    timeout: Optional[float] = None,
) -> OpenAI:
    key = api_key or get_openai_api_key()
    org = organization or get_openai_organization()
    proj = project or get_openai_project()
    url = base_url or OPENAI_API_BASE
    kwargs: Dict[str, Any] = {
        "api_key": key,
        "base_url": url,
    }
    if org:
        kwargs["organization"] = org
    if proj:
        kwargs["project"] = proj
    if timeout is not None:
        kwargs["timeout"] = timeout
    return OpenAI(**kwargs)


def create_async_openai_client(
    api_key: Optional[str] = None,
    organization: Optional[str] = None,
    project: Optional[str] = None,
    base_url: Optional[str] = None,
    timeout: Optional[float] = None,
) -> AsyncOpenAI:
    key = api_key or get_openai_api_key()
    org = organization or get_openai_organization()
    proj = project or get_openai_project()
    url = base_url or OPENAI_API_BASE
    kwargs: Dict[str, Any] = {
        "api_key": key,
        "base_url": url,
    }
    if org:
        kwargs["organization"] = org
    if proj:
        kwargs["project"] = proj
    if timeout is not None:
        kwargs["timeout"] = timeout
    return AsyncOpenAI(**kwargs)


def get_default_model() -> str:
    return os.environ.get("OPENAI_DEFAULT_MODEL", DEFAULT_MODEL)


def get_default_temperature() -> float:
    env_val = os.environ.get("OPENAI_DEFAULT_TEMPERATURE")
    if env_val is not None:
        return float(env_val)
    return DEFAULT_TEMPERATURE


def get_default_max_tokens() -> int:
    env_val = os.environ.get("OPENAI_DEFAULT_MAX_TOKENS")
    if env_val is not None:
        return int(env_val)
    return DEFAULT_MAX_TOKENS


def validate_openai_model_id(model_id: str) -> bool:
    valid_prefixes = (
        "gpt-4",
        "gpt-3.5",
        "text-embedding",
        "tts",
        "whisper",
        "dall-e",
        "o1",
        "o3",
        "o4",
    )
    return any(model_id.startswith(prefix) for prefix in valid_prefixes)
