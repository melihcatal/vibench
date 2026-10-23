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
    diarization_config: Optional[types.SpeakerDiarizationConfig] = None
    enable_word_time_offsets: bool = False
    enable_automatic_punctuation: bool = True


class SpeechClient:
    def __init__(self, config: Optional[TranscriptionConfig] = None):
        self.client = speech.SpeechClient()
        self.config = config or TranscriptionConfig()

    def submit_transcription(self, audio_uri: str) -> str:
        audio = types.RecognitionAudio(uri=audio_uri)
        features = types.RecognitionFeatures(
            enable_speaker_diarization=self.config.diarization_config is not None,
            diarization_config=self.config.diarization_config,
            enable_word_time_offsets=self.config.enable_word_time_offsets,
            enable_automatic_punctuation=self.config.enable_automatic_punctuation,
        )
        config = types.RecognitionConfig(
            encoding=types.RecognitionConfig.AudioEncoding.LINEAR16,
            language_code=self.config.language_code,
            model=self.config.model,
            use_enhanced=self.config.use_enhanced,
            features=features,
        )
        operation = self.client.long_running_recognize(config=config, audio=audio)
        return operation.name
