from __future__ import annotations

import os
from typing import Dict

from openai import OpenAI


OPENAI_BASE_URL = "https://api.openai.com/v1"
OPENAI_DEFAULT_MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
OPENAI_DEFAULT_EMBEDDING_MODEL = os.getenv(
    "OPENAI_EMBEDDING_MODEL", "text-embedding-3-small"
)
OPENAI_DEFAULT_MODERATION_MODEL = os.getenv(
    "OPENAI_MODERATION_MODEL", "omni-moderation-latest"
)
OPENAI_DEFAULT_TTS_MODEL = os.getenv("OPENAI_TTS_MODEL", "gpt-4o-mini-tts")


def get_openai_client() -> OpenAI:
    api_key = os.environ["OPENAI_API_KEY"]
    return OpenAI(api_key=api_key, base_url=OPENAI_BASE_URL)


def get_platform_defaults() -> Dict[str, str]:
    return {
        "model": OPENAI_DEFAULT_MODEL,
        "embedding_model": OPENAI_DEFAULT_EMBEDDING_MODEL,
        "moderation_model": OPENAI_DEFAULT_MODERATION_MODEL,
        "tts_model": OPENAI_DEFAULT_TTS_MODEL,
    }
