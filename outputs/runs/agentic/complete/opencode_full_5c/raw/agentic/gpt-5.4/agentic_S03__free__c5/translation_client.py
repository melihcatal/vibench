from __future__ import annotations

import os
from typing import Any

import requests

from translation_models import normalize_language_code


GOOGLE_TRANSLATE_ENDPOINT = "https://translation.googleapis.com/language/translate/v2"
GOOGLE_TRANSLATE_DETECT_ENDPOINT = (
    "https://translation.googleapis.com/language/translate/v2/detect"
)
GOOGLE_CLOUD_TTS_ENDPOINT = "https://texttospeech.googleapis.com/v1/text:synthesize"
OPENAI_EMBEDDINGS_ENDPOINT = "https://api.openai.com/v1/embeddings"
OPENAI_RESPONSES_ENDPOINT = "https://api.openai.com/v1/responses"
PERSPECTIVE_ANALYZE_ENDPOINT = (
    "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
)


class TranslationClient:
    def __init__(
        self, api_key: str | None = None, session: requests.Session | None = None
    ) -> None:
        self.api_key = api_key or os.environ["GOOGLE_CLOUD_API_KEY"]
        self.session = session or requests.Session()

    def translate(
        self,
        text: str,
        source_language: str,
        target_language: str,
        mime_type: str = "text/plain",
    ) -> dict[str, Any]:
        response = self.session.post(
            GOOGLE_TRANSLATE_ENDPOINT,
            params={"key": self.api_key},
            json={
                "q": text,
                "source": normalize_language_code(source_language),
                "target": normalize_language_code(target_language),
                "format": "html" if mime_type == "text/html" else "text",
            },
            timeout=30,
        )
        response.raise_for_status()
        return response.json()["data"]["translations"][0]

    def translate_many(
        self,
        texts: list[str],
        source_language: str,
        target_language: str,
        mime_type: str = "text/plain",
    ) -> list[dict[str, Any]]:
        response = self.session.post(
            GOOGLE_TRANSLATE_ENDPOINT,
            params={"key": self.api_key},
            json={
                "q": texts,
                "source": normalize_language_code(source_language),
                "target": normalize_language_code(target_language),
                "format": "html" if mime_type == "text/html" else "text",
            },
            timeout=30,
        )
        response.raise_for_status()
        return response.json()["data"]["translations"]


def openai_headers(api_key: str | None = None) -> dict[str, str]:
    key = api_key or os.environ["OPENAI_API_KEY"]
    return {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}


def perspective_params(api_key: str | None = None) -> dict[str, str]:
    return {"key": api_key or os.environ["PERSPECTIVE_API_KEY"]}
