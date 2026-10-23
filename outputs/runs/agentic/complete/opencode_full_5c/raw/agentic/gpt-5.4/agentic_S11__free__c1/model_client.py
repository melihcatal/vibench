from __future__ import annotations

import os
from typing import Optional

from openai import OpenAI


DEFAULT_RESPONSES_MODEL = "gpt-4.1-mini"
DEFAULT_EMBEDDING_MODEL = "text-embedding-3-small"
DEFAULT_TTS_MODEL = "gpt-4o-mini-tts"
DEFAULT_TTS_VOICE = "alloy"
OPENAI_BASE_URL = "https://api.openai.com/v1"


def get_openai_client(api_key: Optional[str] = None) -> OpenAI:
    return OpenAI(
        api_key=api_key or os.environ["OPENAI_API_KEY"],
        base_url=os.environ.get("OPENAI_BASE_URL", OPENAI_BASE_URL),
        organization=os.environ.get("OPENAI_ORG_ID"),
        project=os.environ.get("OPENAI_PROJECT_ID"),
    )


def get_responses_model() -> str:
    return os.environ.get("OPENAI_RESPONSES_MODEL", DEFAULT_RESPONSES_MODEL)


def get_embedding_model() -> str:
    return os.environ.get("OPENAI_EMBEDDING_MODEL", DEFAULT_EMBEDDING_MODEL)


def get_tts_model() -> str:
    return os.environ.get("OPENAI_TTS_MODEL", DEFAULT_TTS_MODEL)


def get_tts_voice() -> str:
    return os.environ.get("OPENAI_TTS_VOICE", DEFAULT_TTS_VOICE)
