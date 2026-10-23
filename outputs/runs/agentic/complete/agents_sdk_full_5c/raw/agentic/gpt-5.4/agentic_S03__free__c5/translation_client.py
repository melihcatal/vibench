from __future__ import annotations

import os
from typing import Any

import requests
from google.cloud import translate_v2 as google_translate
from openai import OpenAI


GOOGLE_CLOUD_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
OPENAI_TTS_MODEL = os.getenv("OPENAI_TTS_MODEL", "gpt-4o-mini-tts")
PERSPECTIVE_API_KEY = os.getenv("PERSPECTIVE_API_KEY")
PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def get_google_translate_client() -> google_translate.Client:
    if GOOGLE_CLOUD_PROJECT:
        return google_translate.Client(project=GOOGLE_CLOUD_PROJECT)
    return google_translate.Client()


def translate_with_google(
    text: str,
    target_language: str,
    source_language: str | None = None,
    format_: str = "text",
) -> dict[str, Any]:
    client = get_google_translate_client()
    params: dict[str, Any] = {
        "target_language": target_language,
        "format_": format_,
    }
    if source_language:
        params["source_language"] = source_language
    return client.translate(text, **params)


def batch_translate_with_google(
    texts: list[str],
    target_language: str,
    source_language: str | None = None,
    format_: str = "text",
) -> list[dict[str, Any]]:
    client = get_google_translate_client()
    params: dict[str, Any] = {
        "target_language": target_language,
        "format_": format_,
    }
    if source_language:
        params["source_language"] = source_language
    result = client.translate(texts, **params)
    if isinstance(result, list):
        return result
    return [result]


def get_openai_client() -> OpenAI:
    return OpenAI(api_key=OPENAI_API_KEY)


def perspective_analyze(text: str) -> dict[str, Any]:
    if not PERSPECTIVE_API_KEY:
        raise ValueError("PERSPECTIVE_API_KEY is required")
    response = requests.post(
        PERSPECTIVE_API_URL,
        params={"key": PERSPECTIVE_API_KEY},
        json={
            "comment": {"text": text},
            "languages": ["en"],
            "requestedAttributes": {
                "TOXICITY": {},
                "INSULT": {},
                "THREAT": {},
                "SEXUALLY_EXPLICIT": {},
            },
        },
        timeout=30,
    )
    response.raise_for_status()
    return response.json()
