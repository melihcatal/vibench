import os
from typing import Any, Dict, List, Optional

from openai import OpenAI


def get_openai_client() -> OpenAI:
    return OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def moderation_model() -> str:
    return os.environ.get("OPENAI_MODERATION_MODEL", "omni-moderation-latest")


def text_to_messages(text: str) -> List[Dict[str, str]]:
    return [{"role": "user", "content": text}]


def threshold_for(category: str, thresholds: Optional[Dict[str, float]]) -> float:
    if thresholds and category in thresholds:
        return float(thresholds[category])
    return 0.5
