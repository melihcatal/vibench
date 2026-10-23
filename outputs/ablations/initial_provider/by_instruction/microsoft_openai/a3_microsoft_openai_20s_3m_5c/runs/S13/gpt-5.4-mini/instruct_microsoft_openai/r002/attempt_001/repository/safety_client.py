import os
from typing import Any, Dict, List, Optional

from openai import OpenAI


OPENAI_MODERATION_MODEL = os.getenv("OPENAI_MODERATION_MODEL", "omni-moderation-latest")


def build_client() -> OpenAI:
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def moderation_thresholds() -> Dict[str, float]:
    return {
        "hate": float(os.getenv("SAFETY_THRESHOLD_HATE", "0.5")),
        "harassment": float(os.getenv("SAFETY_THRESHOLD_HARASSMENT", "0.5")),
        "self_harm": float(os.getenv("SAFETY_THRESHOLD_SELF_HARM", "0.5")),
        "sexual": float(os.getenv("SAFETY_THRESHOLD_SEXUAL", "0.5")),
        "violence": float(os.getenv("SAFETY_THRESHOLD_VIOLENCE", "0.5")),
    }


def moderate_with_openai(client: OpenAI, input_texts: List[str]) -> Any:
    return client.moderations.create(model=OPENAI_MODERATION_MODEL, input=input_texts)


def get_response_item(response: Any, index: int = 0) -> Any:
    return response.results[index]
