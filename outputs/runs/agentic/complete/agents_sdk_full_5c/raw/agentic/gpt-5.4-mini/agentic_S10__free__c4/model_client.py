from __future__ import annotations

import os
from functools import lru_cache

from openai import OpenAI

OPENAI_BASE_URL = os.environ.get("OPENAI_BASE_URL")
DEFAULT_TEXT_MODEL = os.environ.get("OPENAI_TEXT_MODEL", "gpt-4.1-mini")
DEFAULT_REASONING_MODEL = os.environ.get("OPENAI_REASONING_MODEL", "gpt-4.1")
DEFAULT_STRUCTURED_MODEL = os.environ.get("OPENAI_STRUCTURED_MODEL", "gpt-4.1-mini")
DEFAULT_EMBEDDING_MODEL = os.environ.get("OPENAI_EMBEDDING_MODEL", "text-embedding-3-large")
DEFAULT_TRANSLATION_MODEL = os.environ.get("OPENAI_TRANSLATION_MODEL", "gpt-4.1-mini")
DEFAULT_SAFETY_MODEL = os.environ.get("OPENAI_SAFETY_MODEL", "omni-moderation-latest")
DEFAULT_SPOKEN_MODEL = os.environ.get("OPENAI_SPOKEN_MODEL", "gpt-4.1-mini")


@lru_cache(maxsize=1)
def build_openai_client() -> OpenAI:
    if OPENAI_BASE_URL:
        return OpenAI(base_url=OPENAI_BASE_URL)
    return OpenAI()


def resolve_text_model() -> str:
    return DEFAULT_TEXT_MODEL


def resolve_reasoning_model() -> str:
    return DEFAULT_REASONING_MODEL


def resolve_structured_model() -> str:
    return DEFAULT_STRUCTURED_MODEL


def resolve_embedding_model() -> str:
    return DEFAULT_EMBEDDING_MODEL


def resolve_translation_model() -> str:
    return DEFAULT_TRANSLATION_MODEL


def resolve_safety_model() -> str:
    return DEFAULT_SAFETY_MODEL


def resolve_spoken_model() -> str:
    return DEFAULT_SPOKEN_MODEL
