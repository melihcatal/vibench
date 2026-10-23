from __future__ import annotations

import os
from typing import Any, Dict, Optional

import requests


GOOGLE_TTS_ENDPOINT = "https://texttospeech.googleapis.com/v1/text:synthesize"
GOOGLE_VOICES_ENDPOINT = "https://texttospeech.googleapis.com/v1/voices"
GOOGLE_TRANSLATE_ENDPOINT = "https://translation.googleapis.com/language/translate/v2"


class GoogleSpeechClient:
    def __init__(self, api_key: Optional[str] = None, timeout: int = 30) -> None:
        self.api_key = api_key or os.getenv("GOOGLE_CLOUD_API_KEY") or os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("Missing GOOGLE_CLOUD_API_KEY or GOOGLE_API_KEY")
        self.timeout = timeout

    def _request(self, method: str, url: str, *, params: Optional[Dict[str, Any]] = None, json_body: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        merged_params = dict(params or {})
        merged_params["key"] = self.api_key
        response = requests.request(
            method=method,
            url=url,
            params=merged_params,
            json=json_body,
            timeout=self.timeout,
        )
        response.raise_for_status()
        return response.json()

    def synthesize(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        return self._request("POST", GOOGLE_TTS_ENDPOINT, json_body=payload)

    def list_voices(self, language_code: Optional[str] = None) -> Dict[str, Any]:
        params: Dict[str, Any] = {}
        if language_code:
            params["languageCode"] = language_code
        return self._request("GET", GOOGLE_VOICES_ENDPOINT, params=params)

    def translate(self, text: str, target_language: str, source_language: Optional[str] = None, fmt: str = "text") -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "q": text,
            "target": target_language,
            "format": fmt,
        }
        if source_language:
            payload["source"] = source_language
        return self._request("POST", GOOGLE_TRANSLATE_ENDPOINT, json_body=payload)
