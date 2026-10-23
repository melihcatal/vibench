import os
from typing import Dict
from openai import OpenAI

DEFAULT_MODERATION_MODEL = os.getenv("OPENAI_MODERATION_MODEL", "omni-moderation-latest")


def get_openai_client() -> OpenAI:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is required")
    return OpenAI(api_key=api_key)


def get_moderation_model() -> str:
    return os.getenv("OPENAI_MODERATION_MODEL", DEFAULT_MODERATION_MODEL)


def get_thresholds() -> Dict[str, float]:
    raw = os.getenv("SAFETY_CATEGORY_THRESHOLDS", "")
    if not raw:
        return {"hate": 0.5, "harassment": 0.5, "self-harm": 0.5, "sexual": 0.5, "violence": 0.5}
    thresholds: Dict[str, float] = {}
    for item in raw.split(","):
        if not item.strip() or ":" not in item:
            continue
        key, value = item.split(":", 1)
        thresholds[key.strip()] = float(value.strip())
    return thresholds
