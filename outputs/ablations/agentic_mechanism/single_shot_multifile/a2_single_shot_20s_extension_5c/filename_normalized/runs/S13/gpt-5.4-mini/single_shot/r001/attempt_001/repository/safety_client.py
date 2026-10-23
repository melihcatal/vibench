from __future__ import annotations
from functools import lru_cache
from typing import Dict
import os
from openai import OpenAI

DEFAULT_MODERATION_MODEL = os.getenv("OPENAI_MODERATION_MODEL", "omni-moderation-latest")


@lru_cache(maxsize=1)
def get_openai_client() -> OpenAI:
    return OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def get_moderation_model_name() -> str:
    return os.getenv("OPENAI_MODERATION_MODEL", DEFAULT_MODERATION_MODEL)


def get_category_thresholds() -> Dict[str, float]:
    raw = os.getenv("OPENAI_MODERATION_THRESHOLDS", "")
    if not raw:
        return {
            "harassment": 0.7,
            "hate": 0.7,
            "self-harm": 0.6,
            "sexual": 0.7,
            "violence": 0.8,
        }
    thresholds: Dict[str, float] = {}
    for item in raw.split(","):
        if not item.strip() or ":" not in item:
            continue
        key, value = item.split(":", 1)
        thresholds[key.strip()] = float(value.strip())
    return thresholds
