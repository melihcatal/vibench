from __future__ import annotations

import os
from typing import Any, Dict, Optional

import requests
from google.oauth2 import service_account
from google.auth.transport.requests import Request

GOOGLE_TTS_SCOPE = "https://www.googleapis.com/auth/cloud-platform"
GOOGLE_TTS_BASE_URL = "https://texttospeech.googleapis.com/v1"


class GoogleSpeechConfig:
    def __init__(self) -> None:
        self.credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        self.project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
        if not self.credentials_path:
            raise ValueError("GOOGLE_APPLICATION_CREDENTIALS is required")


class GoogleSpeechClient:
    def __init__(self, config: Optional[GoogleSpeechConfig] = None) -> None:
        self.config = config or GoogleSpeechConfig()
        self._credentials = service_account.Credentials.from_service_account_file(
            self.config.credentials_path,
            scopes=[GOOGLE_TTS_SCOPE],
        )

    def _token(self) -> str:
        if not self._credentials.valid:
            self._credentials.refresh(Request())
        return self._credentials.token

    def _headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self._token()}",
            "Content-Type": "application/json",
        }

    def post(self, path: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        response = requests.post(
            f"{GOOGLE_TTS_BASE_URL}{path}",
            json=payload,
            headers=self._headers(),
            timeout=60,
        )
        response.raise_for_status()
        return response.json()

    def get(self, path: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        response = requests.get(
            f"{GOOGLE_TTS_BASE_URL}{path}",
            params=params,
            headers=self._headers(),
            timeout=60,
        )
        response.raise_for_status()
        return response.json()


def build_voice_params(language_code: str, voice_name: Optional[str] = None, gender: Optional[str] = None) -> Dict[str, Any]:
    voice: Dict[str, Any] = {"languageCode": language_code}
    if voice_name:
        voice["name"] = voice_name
    if gender:
        voice["ssmlGender"] = gender
    return voice


def build_audio_config(
    audio_encoding: str = "MP3",
    speaking_rate: float = 1.0,
    pitch: float = 0.0,
    sample_rate_hertz: Optional[int] = None,
) -> Dict[str, Any]:
    config: Dict[str, Any] = {
        "audioEncoding": audio_encoding,
        "speakingRate": speaking_rate,
        "pitch": pitch,
    }
    if sample_rate_hertz is not None:
        config["sampleRateHertz"] = sample_rate_hertz
    return config
