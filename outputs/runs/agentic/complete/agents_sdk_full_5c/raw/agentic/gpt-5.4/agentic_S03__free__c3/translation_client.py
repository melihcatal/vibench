from __future__ import annotations

import os
from typing import Optional

import deepl
from openai import OpenAI
from elevenlabs.client import ElevenLabs


DEEPL_AUTH_KEY_ENV = "DEEPL_AUTH_KEY"
OPENAI_API_KEY_ENV = "OPENAI_API_KEY"
ELEVENLABS_API_KEY_ENV = "ELEVENLABS_API_KEY"


class TranslationServiceConfigError(RuntimeError):
    pass


def _get_required_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise TranslationServiceConfigError(f"Missing required environment variable: {name}")
    return value


def get_deepl_client(auth_key: Optional[str] = None) -> deepl.Translator:
    key = auth_key or _get_required_env(DEEPL_AUTH_KEY_ENV)
    return deepl.Translator(auth_key=key)


def get_openai_client(api_key: Optional[str] = None) -> OpenAI:
    key = api_key or _get_required_env(OPENAI_API_KEY_ENV)
    return OpenAI(api_key=key)


def get_elevenlabs_client(api_key: Optional[str] = None) -> ElevenLabs:
    key = api_key or _get_required_env(ELEVENLABS_API_KEY_ENV)
    return ElevenLabs(api_key=key)
