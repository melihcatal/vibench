from __future__ import annotations

import os
from typing import Optional

from google.cloud import translate_v3
from openai import OpenAI


DEFAULT_GOOGLE_LOCATION = os.getenv("GOOGLE_TRANSLATE_LOCATION", "global")
DEFAULT_GOOGLE_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT") or os.getenv("GCP_PROJECT")
DEFAULT_OPENAI_MODEL = os.getenv("OPENAI_SUMMARY_MODEL", "gpt-4o-mini")
DEFAULT_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
DEFAULT_ELEVENLABS_MODEL = os.getenv("ELEVENLABS_TTS_MODEL", "eleven_multilingual_v2")
DEFAULT_ELEVENLABS_VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID", "EXAVITQu4vr4xnSDxMaL")


def require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise ValueError(f"Missing required environment variable: {name}")
    return value


def get_translate_client() -> translate_v3.TranslationServiceClient:
    return translate_v3.TranslationServiceClient()


def get_google_parent(project_id: Optional[str] = None, location: Optional[str] = None) -> str:
    resolved_project = project_id or DEFAULT_GOOGLE_PROJECT
    if not resolved_project:
        raise ValueError("Set GOOGLE_CLOUD_PROJECT or pass project_id")
    resolved_location = location or DEFAULT_GOOGLE_LOCATION
    return f"projects/{resolved_project}/locations/{resolved_location}"


def get_openai_client() -> OpenAI:
    require_env("OPENAI_API_KEY")
    return OpenAI()


def get_elevenlabs_headers() -> dict:
    return {
        "xi-api-key": require_env("ELEVENLABS_API_KEY"),
        "Content-Type": "application/json",
        "Accept": "audio/mpeg",
    }
