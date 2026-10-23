import os
from functools import lru_cache

from openai import OpenAI


DEFAULT_OPENAI_MODERATION_MODEL = os.getenv("OPENAI_MODERATION_MODEL", "omni-moderation-latest")


@lru_cache(maxsize=1)
def get_openai_client() -> OpenAI:
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def get_moderation_model() -> str:
    return DEFAULT_OPENAI_MODERATION_MODEL


def get_category_thresholds() -> dict:
    return {
        "harassment": float(os.getenv("SAFETY_THRESHOLD_HARASSMENT", "0.75")),
        "hate": float(os.getenv("SAFETY_THRESHOLD_HATE", "0.75")),
        "self-harm": float(os.getenv("SAFETY_THRESHOLD_SELF_HARM", "0.5")),
        "sexual": float(os.getenv("SAFETY_THRESHOLD_SEXUAL", "0.8")),
        "violence": float(os.getenv("SAFETY_THRESHOLD_VIOLENCE", "0.7")),
    }
