from __future__ import annotations

import os
from typing import Optional

import requests
from openai import OpenAI
from elevenlabs.client import ElevenLabs


AZURE_TRANSLATOR_ENDPOINT = os.getenv("AZURE_TRANSLATOR_ENDPOINT", "https://api.cognitive.microsofttranslator.com")
AZURE_TRANSLATOR_KEY = os.getenv("AZURE_TRANSLATOR_KEY")
AZURE_TRANSLATOR_REGION = os.getenv("AZURE_TRANSLATOR_REGION")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
ELEVENLABS_VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID", "JBFqnCBsd6RMkjVDRZzb")


def _require(value: Optional[str], name: str) -> str:
    if not value:
        raise ValueError(f"Missing required environment variable: {name}")
    return value


def translator_headers() -> dict:
    headers = {
        "Ocp-Apim-Subscription-Key": _require(AZURE_TRANSLATOR_KEY, "AZURE_TRANSLATOR_KEY"),
        "Content-Type": "application/json",
    }
    if AZURE_TRANSLATOR_REGION:
        headers["Ocp-Apim-Subscription-Region"] = AZURE_TRANSLATOR_REGION
    return headers


def translator_url(path: str = "/translate") -> str:
    return f"{AZURE_TRANSLATOR_ENDPOINT.rstrip('/')}{path}"


def translator_session() -> requests.Session:
    session = requests.Session()
    session.headers.update(translator_headers())
    return session


def openai_client() -> OpenAI:
    return OpenAI(api_key=_require(OPENAI_API_KEY, "OPENAI_API_KEY"))


def elevenlabs_client() -> ElevenLabs:
    return ElevenLabs(api_key=_require(ELEVENLABS_API_KEY, "ELEVENLABS_API_KEY"))
