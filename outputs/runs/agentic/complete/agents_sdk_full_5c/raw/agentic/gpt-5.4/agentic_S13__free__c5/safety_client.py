from __future__ import annotations

import os
from typing import Optional

from openai import OpenAI


OPENAI_API_KEY_ENV = "OPENAI_API_KEY"
OPENAI_MODERATION_MODEL = "omni-moderation-latest"
OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"
OPENAI_TTS_MODEL = "gpt-4o-mini-tts"
OPENAI_TRANSLATION_MODEL = "gpt-4o-mini"
OPENAI_SUMMARY_MODEL = "gpt-4o-mini"


def get_openai_client(api_key: Optional[str] = None) -> OpenAI:
    key = api_key or os.getenv(OPENAI_API_KEY_ENV)
    if not key:
        raise RuntimeError(f"Missing required environment variable: {OPENAI_API_KEY_ENV}")
    return OpenAI(api_key=key)


def get_category_thresholds() -> dict:
    return {
        "hate": 0.5,
        "hate/threatening": 0.2,
        "harassment": 0.6,
        "harassment/threatening": 0.25,
        "self-harm": 0.35,
        "self-harm/intent": 0.2,
        "self-harm/instructions": 0.15,
        "sexual": 0.75,
        "sexual/minors": 0.01,
        "violence": 0.65,
        "violence/graphic": 0.3,
    }
