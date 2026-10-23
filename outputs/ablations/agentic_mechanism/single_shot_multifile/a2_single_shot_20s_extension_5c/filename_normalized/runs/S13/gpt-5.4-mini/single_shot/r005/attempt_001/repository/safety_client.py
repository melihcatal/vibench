import os
from functools import lru_cache
from typing import Dict
from openai import OpenAI


def provider_name() -> str:
    return "openai"


@lru_cache(maxsize=1)
def build_openai_client() -> OpenAI:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is required")
    return OpenAI(api_key=api_key)


def get_category_thresholds() -> Dict[str, float]:
    return {
        "hate": float(os.getenv("SAFETY_THRESHOLD_HATE", "0.50")),
        "harassment": float(os.getenv("SAFETY_THRESHOLD_HARASSMENT", "0.50")),
        "self-harm": float(os.getenv("SAFETY_THRESHOLD_SELF_HARM", "0.50")),
        "sexual": float(os.getenv("SAFETY_THRESHOLD_SEXUAL", "0.50")),
        "violence": float(os.getenv("SAFETY_THRESHOLD_VIOLENCE", "0.50")),
    }
