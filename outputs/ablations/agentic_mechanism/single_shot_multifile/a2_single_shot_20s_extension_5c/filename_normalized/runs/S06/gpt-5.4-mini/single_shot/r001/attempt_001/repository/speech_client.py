from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any

from google.cloud import texttospeech

from speech_models import AudioResponse, VoiceInfo, VoiceSelectionRequest, normalize_locale


@dataclass
class TTSConfig:
    project_id: str | None = None
    location: str = 'global'
    language_code: str | None = None
    default_voice: str | None = None


def load_config() -> TTSConfig:
    return TTSConfig(
        project_id=os.getenv('GOOGLE_CLOUD_PROJECT') or os.getenv('GCP_PROJECT'),
        location=os.getenv('GOOGLE_CLOUD_LOCATION', 'global'),
        language_code=os.getenv('TTS_LANGUAGE_CODE'),
        default_voice=os.getenv('TTS_VOICE_NAME'),
    )


class GoogleCloudTTSClient:
    def __init__(self, config: TTSConfig | None = None):
        self.config = config or load_config()
        self.client = texttospeech.TextToSpeechClient()

    def synthesize_text(self, request: Any) -> AudioResponse:
        input_text = texttospeech.SynthesisInput(text=request.text)
        voice_params = texttospeech.VoiceSelectionParams(
            language_code=request.locale or self.config.language_code or 'en-US',
            name=request.voice or self.config.default_voice or '',
        )
        audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
        response = self.client.synthesize_speech(input=input_text, voice=voice_params, audio_config=audio_config)
        return AudioResponse(audio=response.audio_content, content_type='audio/mpeg')

    def synthesize_ssml(self, request: Any) -> AudioResponse:
        input_ssml = texttospeech.SynthesisInput(ssml=request.ssml)
        voice_params = texttospeech.VoiceSelectionParams(
            language_code=request.locale or self.config.language_code or 'en-US',
            name=request.voice or self.config.default_voice or '',
        )
        audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
        response = self.client.synthesize_speech(input=input_ssml, voice=voice_params, audio_config=audio_config)
        return AudioResponse(audio=response.audio_content, content_type='audio/mpeg')

    def list_voices(self, request: VoiceSelectionRequest):
        language_code = normalize_locale(request.locale)
        response = self.client.list_voices(language_code=language_code)
        return [VoiceInfo(name=v.name, language_codes=list(v.language_codes), ssml_gender=str(v.ssml_gender)) for v in response.voices]

    def get_voice(self, request: VoiceSelectionRequest):
        voices = self.list_voices(request)
        if request.voice_name:
            for voice in voices:
                if voice.name == request.voice_name:
                    return voice
        return voices[0] if voices else None


def build_tts_client(config: TTSConfig | None = None) -> GoogleCloudTTSClient:
    return GoogleCloudTTSClient(config=config)
