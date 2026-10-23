from __future__ import annotations

import os
from typing import Optional

from google.cloud import texttospeech

from speech_models import normalize_audio_encoding


DEFAULT_TTS_VOICE = os.getenv("GOOGLE_TTS_VOICE", "en-US-Neural2-F")
DEFAULT_TTS_LANGUAGE = os.getenv("GOOGLE_TTS_LANGUAGE", "en-US")
DEFAULT_TTS_MODEL = os.getenv("GOOGLE_TTS_MODEL", "default")


class GoogleTTSClientFactory:
    @staticmethod
    def create_client() -> texttospeech.TextToSpeechClient:
        return texttospeech.TextToSpeechClient()

    @staticmethod
    def audio_encoding_for(audio_encoding: str) -> texttospeech.AudioEncoding:
        normalized = normalize_audio_encoding(audio_encoding)
        mapping = {
            "mp3": texttospeech.AudioEncoding.MP3,
            "ogg_opus": texttospeech.AudioEncoding.OGG_OPUS,
            "pcm": texttospeech.AudioEncoding.LINEAR16,
            "mulaw": texttospeech.AudioEncoding.MULAW,
            "alaw": texttospeech.AudioEncoding.ALAW,
        }
        if normalized not in mapping:
            raise ValueError(f"Unsupported Google Cloud Text-to-Speech encoding: {audio_encoding}")
        return mapping[normalized]

    @staticmethod
    def voice_params(voice_name: Optional[str], language_code: Optional[str]) -> texttospeech.VoiceSelectionParams:
        name = voice_name or DEFAULT_TTS_VOICE
        language = language_code or DEFAULT_TTS_LANGUAGE
        params = texttospeech.VoiceSelectionParams(language_code=language, name=name)
        if DEFAULT_TTS_MODEL:
            params.model_name = DEFAULT_TTS_MODEL
        return params
