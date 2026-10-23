from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

from openai import OpenAI

DEFAULT_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
DEFAULT_EMBED_MODEL = os.getenv("OPENAI_EMBED_MODEL", "text-embedding-3-small")


@dataclass(frozen=True)
class LLMConfig:
    api_key: Optional[str] = None
    model: str = DEFAULT_MODEL
    base_url: Optional[str] = None


def get_openai_client(config: Optional[LLMConfig] = None) -> OpenAI:
    cfg = config or LLMConfig(api_key=os.getenv("OPENAI_API_KEY"))
    kwargs: Dict[str, Any] = {}
    if cfg.api_key:
        kwargs["api_key"] = cfg.api_key
    if cfg.base_url:
        kwargs["base_url"] = cfg.base_url
    return OpenAI(**kwargs)


def get_model_name(model: Optional[str] = None) -> str:
    return model or DEFAULT_MODEL


def get_embedding_model_name(model: Optional[str] = None) -> str:
    return model or DEFAULT_EMBED_MODEL
