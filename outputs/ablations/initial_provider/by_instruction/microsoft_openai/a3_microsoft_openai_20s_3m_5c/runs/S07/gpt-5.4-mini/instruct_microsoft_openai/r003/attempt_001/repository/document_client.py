import os
from dataclasses import dataclass
from typing import Optional

from openai import OpenAI


@dataclass
class DocumentClientConfig:
    openai_api_key: Optional[str] = None
    openai_base_url: Optional[str] = None
    openai_model: str = "gpt-5.4-mini"


def load_config() -> DocumentClientConfig:
    return DocumentClientConfig(
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        openai_base_url=os.getenv("OPENAI_BASE_URL"),
        openai_model=os.getenv("OPENAI_MODEL", "gpt-5.4-mini"),
    )


def create_client() -> OpenAI:
    cfg = load_config()
    kwargs = {}
    if cfg.openai_api_key:
        kwargs["api_key"] = cfg.openai_api_key
    if cfg.openai_base_url:
        kwargs["base_url"] = cfg.openai_base_url
    return OpenAI(**kwargs)
