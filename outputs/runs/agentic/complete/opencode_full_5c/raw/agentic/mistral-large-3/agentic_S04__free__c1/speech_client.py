from google.cloud import speech_v1p1beta1 as speech
from google.cloud.speech_v1p1beta1 import types
import os
from typing import Optional
from dataclasses import dataclass


@dataclass
class TranscriptionConfig:
    language_code: str = "en-US"
    model: str = "latest_long"
    use_enhanced: bool = True
    enable_automatic_punctuation: bool = True
    diarization_config: Optional[types.SpeakerDiarizationConfig] = None


class SpeechClient:
    def __init__(self, config: Optional[TranscriptionConfig] = None):
        self.client = speech.SpeechClient()
        self.config = config or TranscriptionConfig()

    def get_client(self):
        return self.client

    def get_config(self) -> TranscriptionConfig:
        return self.config

    def load_audio(self, file_path: str) -> types.RecognitionAudio:
        with open(file_path, "rb") as audio_file:
            content = audio_file.read()
        return types.RecognitionAudio(content=content)

    def create_recognition_config(self) -> types.RecognitionConfig:
        config = types.RecognitionConfig(
            encoding=types.RecognitionConfig.AudioEncoding.LINEAR16,
            language_code=self.config.language_code,
            model=self.config.model,
            use_enhanced=self.config.use_enhanced,
            enable_automatic_punctuation=self.config.enable_automatic_punctuation,
        )
        if self.config.diarization_config:
            config.diarization_config = self.config.diarization_config
        return config
