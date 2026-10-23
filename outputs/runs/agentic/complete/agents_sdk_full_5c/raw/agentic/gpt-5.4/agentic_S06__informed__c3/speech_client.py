from __future__ import annotations

import os
from typing import Optional

from google.cloud import texttospeech

from speech_models import normalize_audio_encoding, normalize_language_code


class GoogleTTSClient:
    provider = "google-cloud-texttospeech"

    def __init__(self, project_hint: Optional[str] = None) -> None:
        self.project_hint = project_hint or os.getenv("GOOGLE_CLOUD_PROJECT")
        self.credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        self.client = texttospeech.TextToSpeechClient()

    def build_audio_config(
        self,
        audio_encoding: str = "MP3",
        speaking_rate: float = 1.0,
        pitch: float = 0.0,
        sample_rate_hertz: Optional[int] = None,
    ) -> texttospeech.AudioConfig:
        encoding_name = normalize_audio_encoding(audio_encoding)
        encoding = getattr(texttospeech.AudioEncoding, encoding_name)
        payload = {
            "audio_encoding": encoding,
            "speaking_rate": speaking_rate,
            "pitch": pitch,
        }
        if sample_rate_hertz:
            payload["sample_rate_hertz"] = sample_rate_hertz
        return texttospeech.AudioConfig(**payload)

    def build_voice_params(
        self,
        language_code: Optional[str] = "en-US",
        voice_name: Optional[str] = None,
    ) -> texttospeech.VoiceSelectionParams:
        return texttospeech.VoiceSelectionParams(
            language_code=normalize_language_code(language_code),
            name=voice_name or "",
        )


def get_google_tts_client() -> GoogleTTSClient:
    return GoogleTTSClient()
