from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional, Tuple

from openai import OpenAI

DEFAULT_MODEL = "gpt-4o-mini"
DEFAULT_EMBEDDING_MODEL = "text-embedding-3-small"
DEFAULT_TTS_MODEL = "gpt-4o-mini-tts"
DEFAULT_TRANSLATION_MODEL = "gpt-4o-mini"
DEFAULT_SAFETY_MODEL = "gpt-4o-mini"


@dataclass(frozen=True)
class ModelConfig:
    api_key: Optional[str] = None
    model: str = DEFAULT_MODEL
    organization: Optional[str] = None
    base_url: Optional[str] = None


def load_config(model: Optional[str] = None) -> ModelConfig:
    return ModelConfig(
        api_key=os.getenv("OPENAI_API_KEY"),
        model=model or os.getenv("OPENAI_MODEL", DEFAULT_MODEL),
        organization=os.getenv("OPENAI_ORG_ID"),
        base_url=os.getenv("OPENAI_BASE_URL"),
    )


def client_for(config: Optional[ModelConfig] = None) -> OpenAI:
    cfg = config or load_config()
    kwargs: Dict[str, Any] = {}
    if cfg.api_key:
        kwargs["api_key"] = cfg.api_key
    if cfg.organization:
        kwargs["organization"] = cfg.organization
    if cfg.base_url:
        kwargs["base_url"] = cfg.base_url
    return OpenAI(**kwargs)


def model_family(model: Optional[str] = None) -> str:
    name = (model or DEFAULT_MODEL).lower()
    if "gpt-4o" in name:
        return "gpt-4o"
    if "gpt-4.1" in name:
        return "gpt-4.1"
    if "o1" in name:
        return "o1"
    if "embedding" in name:
        return "embedding"
    if "tts" in name:
        return "tts"
    return "generic"


def text_messages(system: str, user: str, extra: Optional[Iterable[Tuple[str, str]]] = None) -> List[Dict[str, str]]:
    messages: List[Dict[str, str]] = [{"role": "system", "content": system}]
    if extra:
        for role, content in extra:
            messages.append({"role": role, "content": content})
    messages.append({"role": "user", "content": user})
    return messages
