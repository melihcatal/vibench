import os
from functools import lru_cache
from typing import Any, Dict, Optional

from openai import OpenAI


def _env(name: str, default: str = "") -> str:
    return os.getenv(name, default).strip()


@lru_cache(maxsize=1)
def get_client() -> OpenAI:
    return OpenAI(api_key=_env("OPENAI_API_KEY") or None)


def default_moderation_model() -> str:
    return _env("OPENAI_MODERATION_MODEL", "omni-moderation-latest")


def default_chat_model() -> str:
    return _env("OPENAI_CHAT_MODEL", "gpt-4.1-mini")


def default_embedding_model() -> str:
    return _env("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")


def default_audio_model() -> str:
    return _env("OPENAI_AUDIO_MODEL", "gpt-4o-mini-tts")


def moderation_thresholds() -> Dict[str, float]:
    return {
        "harassment": float(_env("MODERATION_THRESHOLD_HARASSMENT", "0.5")),
        "hate": float(_env("MODERATION_THRESHOLD_HATE", "0.5")),
        "sexual": float(_env("MODERATION_THRESHOLD_SEXUAL", "0.5")),
        "violence": float(_env("MODERATION_THRESHOLD_VIOLENCE", "0.5")),
        "self_harm": float(_env("MODERATION_THRESHOLD_SELF_HARM", "0.5")),
        "illicit": float(_env("MODERATION_THRESHOLD_ILLICIT", "0.5")),
    }


def map_category_scores(scores: Optional[Dict[str, Any]]) -> Dict[str, float]:
    if not scores:
        return {}
    normalized: Dict[str, float] = {}
    for key, value in scores.items():
        try:
            normalized[str(key)] = float(value)
        except (TypeError, ValueError):
            continue
    return normalized
