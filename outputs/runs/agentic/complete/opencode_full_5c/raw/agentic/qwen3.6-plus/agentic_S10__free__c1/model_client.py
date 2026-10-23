import os
from typing import Optional

from openai import OpenAI, AsyncOpenAI

OPENAI_API_BASE = "https://api.openai.com/v1"


def get_openai_api_key() -> str:
    api_key = os.environ.get("OPENAI_API_KEY", "")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is not set")
    return api_key


def get_openai_organization() -> Optional[str]:
    return os.environ.get("OPENAI_ORGANIZATION_ID")


def create_openai_client(
    api_key: Optional[str] = None, base_url: Optional[str] = None
) -> OpenAI:
    key = api_key or get_openai_api_key()
    url = base_url or OPENAI_API_BASE
    org = get_openai_organization()
    if org:
        return OpenAI(api_key=key, base_url=url, organization=org)
    return OpenAI(api_key=key, base_url=url)


def create_async_openai_client(
    api_key: Optional[str] = None, base_url: Optional[str] = None
) -> AsyncOpenAI:
    key = api_key or get_openai_api_key()
    url = base_url or OPENAI_API_BASE
    org = get_openai_organization()
    if org:
        return AsyncOpenAI(api_key=key, base_url=url, organization=org)
    return AsyncOpenAI(api_key=key, base_url=url)


def load_config() -> dict:
    return {
        "provider": "openai",
        "api_base": os.environ.get("OPENAI_API_BASE", OPENAI_API_BASE),
        "api_key_env": "OPENAI_API_KEY",
        "organization": get_openai_organization(),
        "default_model": os.environ.get("DEFAULT_LLM_MODEL", "gpt-4o"),
        "default_embedding_model": os.environ.get(
            "DEFAULT_EMBEDDING_MODEL", "text-embedding-3-small"
        ),
        "default_moderation_model": os.environ.get(
            "DEFAULT_MODERATION_MODEL", "omni-moderation-latest"
        ),
        "timeout": int(os.environ.get("LLM_REQUEST_TIMEOUT", "120")),
        "max_retries": int(os.environ.get("LLM_MAX_RETRIES", "3")),
    }


def resolve_model(model_hint: str, config: Optional[dict] = None) -> str:
    cfg = config or load_config()
    if model_hint:
        return model_hint
    return cfg.get("default_model", "gpt-4o")


def normalize_payload(messages: list[dict], model: str, **kwargs) -> dict:
    payload = {
        "model": model,
        "messages": messages,
    }
    for key in ("max_tokens", "temperature", "top_p", "stop", "seed", "stream"):
        if key in kwargs and kwargs[key] is not None:
            payload[key] = kwargs[key]
    return payload


def parse_completion_response(raw: dict) -> str:
    choices = raw.get("choices", [])
    if not choices:
        return ""
    return choices[0].get("message", {}).get("content", "")


def parse_usage(raw: dict) -> dict:
    return raw.get("usage", {})
