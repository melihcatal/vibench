from __future__ import annotations

import os
from typing import Dict, Optional

import requests


PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
GOOGLE_TRANSLATE_API_URL = "https://translation.googleapis.com/language/translate/v2"
OPENAI_EMBEDDINGS_API_URL = "https://api.openai.com/v1/embeddings"
ELEVENLABS_TTS_API_URL = "https://api.elevenlabs.io/v1/text-to-speech"


def get_env(name: str, default: Optional[str] = None) -> str:
    value = os.getenv(name, default)
    if value is None or value == "":
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


def perspective_api_key() -> str:
    return get_env("PERSPECTIVE_API_KEY")


def google_api_key() -> str:
    return get_env("GOOGLE_API_KEY")


def openai_api_key() -> str:
    return get_env("OPENAI_API_KEY")


def elevenlabs_api_key() -> str:
    return get_env("ELEVENLABS_API_KEY")


def default_session() -> requests.Session:
    session = requests.Session()
    session.headers.update({"User-Agent": "safety-integrations/1.0"})
    return session


def perspective_requested_attributes() -> Dict[str, Dict[str, str]]:
    return {
        "TOXICITY": {},
        "SEVERE_TOXICITY": {},
        "INSULT": {},
        "PROFANITY": {},
        "THREAT": {},
        "IDENTITY_ATTACK": {},
    }
