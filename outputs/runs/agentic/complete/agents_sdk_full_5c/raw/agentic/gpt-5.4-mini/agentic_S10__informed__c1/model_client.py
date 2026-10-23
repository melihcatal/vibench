from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

from openai import OpenAI

DEFAULT_CHAT_MODEL = os.getenv("LLM_MODEL", "gpt-4.1-mini")
DEFAULT_EMBED_MODEL = os.getenv("LLM_EMBED_MODEL", "text-embedding-3-small")
DEFAULT_TTS_MODEL = os.getenv("LLM_TTS_MODEL", "gpt-4o-mini-tts")


@dataclass(frozen=True)
class LLMConfig:
    api_key: str = os.getenv("OPENAI_API_KEY", "")
    chat_model: str = DEFAULT_CHAT_MODEL
    embed_model: str = DEFAULT_EMBED_MODEL
    tts_model: str = DEFAULT_TTS_MODEL
    base_url: Optional[str] = os.getenv("OPENAI_BASE_URL")


def get_openai_client(config: Optional[LLMConfig] = None) -> OpenAI:
    cfg = config or LLMConfig()
    kwargs: Dict[str, Any] = {"api_key": cfg.api_key or None}
    if cfg.base_url:
        kwargs["base_url"] = cfg.base_url
    return OpenAI(**kwargs)


def model_family(model_name: str) -> str:
    lowered = model_name.lower()
    if lowered.startswith(("gpt-4.1", "gpt-4o", "gpt-4", "o1", "o3")):
        return "openai-gpt-family"
    if "embedding" in lowered:
        return "embedding-family"
    if "tts" in lowered or "audio" in lowered:
        return "speech-family"
    return "general-llm-family"
