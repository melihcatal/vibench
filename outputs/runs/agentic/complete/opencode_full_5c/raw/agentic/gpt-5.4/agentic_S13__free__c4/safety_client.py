from __future__ import annotations

import os
from typing import Any, Sequence

from openai import OpenAI


DEFAULT_MODERATION_MODEL = "omni-moderation-latest"


def get_openai_api_key() -> str:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")
    return api_key


def get_openai_client() -> OpenAI:
    return OpenAI(api_key=get_openai_api_key())


def moderation_model_name() -> str:
    return os.environ.get("OPENAI_MODERATION_MODEL", DEFAULT_MODERATION_MODEL)


def moderation_thresholds() -> dict[str, float]:
    return {
        "violence": float(os.environ.get("SAFETY_THRESHOLD_VIOLENCE", "0.6")),
        "violence/graphic": float(
            os.environ.get("SAFETY_THRESHOLD_VIOLENCE_GRAPHIC", "0.45")
        ),
        "self-harm": float(os.environ.get("SAFETY_THRESHOLD_SELF_HARM", "0.5")),
        "self-harm/intent": float(
            os.environ.get("SAFETY_THRESHOLD_SELF_HARM_INTENT", "0.4")
        ),
        "self-harm/instructions": float(
            os.environ.get("SAFETY_THRESHOLD_SELF_HARM_INSTRUCTIONS", "0.35")
        ),
        "harassment": float(os.environ.get("SAFETY_THRESHOLD_HARASSMENT", "0.75")),
        "harassment/threatening": float(
            os.environ.get("SAFETY_THRESHOLD_HARASSMENT_THREATENING", "0.45")
        ),
        "hate": float(os.environ.get("SAFETY_THRESHOLD_HATE", "0.75")),
        "hate/threatening": float(
            os.environ.get("SAFETY_THRESHOLD_HATE_THREATENING", "0.4")
        ),
        "illicit": float(os.environ.get("SAFETY_THRESHOLD_ILLICIT", "0.55")),
        "illicit/violent": float(
            os.environ.get("SAFETY_THRESHOLD_ILLICIT_VIOLENT", "0.4")
        ),
        "sexual": float(os.environ.get("SAFETY_THRESHOLD_SEXUAL", "0.8")),
        "sexual/minors": float(
            os.environ.get("SAFETY_THRESHOLD_SEXUAL_MINORS", "0.01")
        ),
    }


def create_moderation_input(texts: Sequence[str]) -> list[dict[str, Any]]:
    return [{"type": "text", "text": text} for text in texts]
