from __future__ import annotations

import os
from typing import Any

import requests

from translation_models import ensure_text_list, normalize_language_code


DEEPL_API_URL = "https://api.deepl.com/v2/translate"
OPENAI_RESPONSES_URL = "https://api.openai.com/v1/responses"
OPENAI_EMBEDDINGS_URL = "https://api.openai.com/v1/embeddings"
OPENAI_AUDIO_URL = "https://api.openai.com/v1/audio/speech"
OPENAI_DEFAULT_MODEL = "gpt-4.1-mini"
OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"
OPENAI_TTS_MODEL = "gpt-4o-mini-tts"


def get_deepl_api_key() -> str:
    api_key = os.environ["DEEPL_API_KEY"]
    if not api_key.strip():
        raise ValueError("DEEPL_API_KEY is empty")
    return api_key


def get_openai_api_key() -> str:
    api_key = os.environ["OPENAI_API_KEY"]
    if not api_key.strip():
        raise ValueError("OPENAI_API_KEY is empty")
    return api_key


def _deepl_headers() -> dict[str, str]:
    return {
        "Authorization": f"DeepL-Auth-Key {get_deepl_api_key()}",
        "Content-Type": "application/json",
    }


def _openai_headers() -> dict[str, str]:
    return {
        "Authorization": f"Bearer {get_openai_api_key()}",
        "Content-Type": "application/json",
    }


def deepl_translate(
    texts: list[str],
    target_language: str,
    source_language: str | None = None,
    *,
    tag_handling: str | None = None,
) -> list[dict[str, Any]]:
    payload: dict[str, Any] = {
        "text": ensure_text_list(texts),
        "target_lang": (
            normalize_language_code(target_language) or target_language
        ).upper(),
    }
    normalized_source = normalize_language_code(source_language)
    if normalized_source:
        payload["source_lang"] = normalized_source.upper()
    if tag_handling:
        payload["tag_handling"] = tag_handling
    response = requests.post(
        DEEPL_API_URL, headers=_deepl_headers(), json=payload, timeout=60
    )
    response.raise_for_status()
    body = response.json()
    return body["translations"]


def openai_text_response(
    system_prompt: str, user_input: str, *, temperature: float = 0.0
) -> str:
    payload = {
        "model": OPENAI_DEFAULT_MODEL,
        "input": [
            {
                "role": "system",
                "content": [{"type": "input_text", "text": system_prompt}],
            },
            {"role": "user", "content": [{"type": "input_text", "text": user_input}]},
        ],
        "temperature": temperature,
    }
    response = requests.post(
        OPENAI_RESPONSES_URL, headers=_openai_headers(), json=payload, timeout=60
    )
    response.raise_for_status()
    data = response.json()
    return data["output"][0]["content"][0]["text"]


def openai_embedding(text: str) -> dict[str, Any]:
    payload = {
        "model": OPENAI_EMBEDDING_MODEL,
        "input": text,
    }
    response = requests.post(
        OPENAI_EMBEDDINGS_URL, headers=_openai_headers(), json=payload, timeout=60
    )
    response.raise_for_status()
    data = response.json()
    return data["data"][0]


def openai_speech(
    text: str, *, voice: str = "alloy", audio_format: str = "mp3"
) -> bytes:
    payload = {
        "model": OPENAI_TTS_MODEL,
        "voice": voice,
        "input": text,
        "format": audio_format,
    }
    response = requests.post(
        OPENAI_AUDIO_URL, headers=_openai_headers(), json=payload, timeout=120
    )
    response.raise_for_status()
    return response.content
