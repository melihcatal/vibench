import os
from typing import Any, Dict, Optional

from openai import OpenAI

DEFAULT_MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")


def get_api_key() -> Optional[str]:
    return os.getenv("OPENAI_API_KEY")


def get_base_url() -> Optional[str]:
    return os.getenv("OPENAI_BASE_URL")


def build_client(api_key: Optional[str] = None, base_url: Optional[str] = None) -> OpenAI:
    params: Dict[str, Any] = {}
    key = api_key or get_api_key()
    url = base_url or get_base_url()
    if key:
        params["api_key"] = key
    if url:
        params["base_url"] = url
    return OpenAI(**params)


def generate_text(prompt: str, model: str = DEFAULT_MODEL, system_prompt: Optional[str] = None, temperature: float = 0.2) -> str:
    client = build_client()
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})
    response = client.responses.create(model=model, input=messages, temperature=temperature)
    return response.output_text


def get_model_config() -> Dict[str, str]:
    return {
        "provider": "openai",
        "model": DEFAULT_MODEL,
        "api_key_env": "OPENAI_API_KEY",
        "base_url_env": "OPENAI_BASE_URL",
    }
