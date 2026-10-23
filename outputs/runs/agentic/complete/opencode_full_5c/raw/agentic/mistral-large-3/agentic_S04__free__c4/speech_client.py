from google.cloud import speech_v1p1beta1 as speech
from google.api_core.exceptions import GoogleAPICallError, RetryError
import os
from typing import Optional
from dataclasses import dataclass


@dataclass
class TranscriptionConfig:
    language_code: str = "en-US"
    model: str = "latest_long"
    use_enhanced: bool = True
    diarization_speaker_count: Optional[int] = None
    enable_word_time_offsets: bool = False
    enable_automatic_punctuation: bool = True


class SpeechClient:
    def __init__(self, config: Optional[TranscriptionConfig] = None):
        self.config = config or TranscriptionConfig()
        self.client = speech.SpeechClient()

    def _get_gcs_uri(self, file_path: str) -> str:
        if file_path.startswith("gs://"):
            return file_path
        raise ValueError(
            "Only Google Cloud Storage URIs (gs://) are supported for batch transcription."
        )

    def submit_transcription(self, audio_file_path: str) -> str:
        gcs_uri = self._get_gcs_uri(audio_file_path)
        audio = speech.RecognitionAudio(uri=gcs_uri)

        config = speech.RecognitionConfig(
            language_code=self.config.language_code,
            model=self.config.model,
            use_enhanced=self.config.use_enhanced,
            enable_automatic_punctuation=self.config.enable_automatic_punctuation,
            diarization_config=speech.SpeakerDiarizationConfig(
                enable_speaker_diarization=self.config.diarization_speaker_count
                is not None,
                min_speaker_count=self.config.diarization_speaker_count,
                max_speaker_count=self.config.diarization_speaker_count,
            )
            if self.config.diarization_speaker_count
            else None,
            enable_word_time_offsets=self.config.enable_word_time_offsets,
        )

        operation = self.client.long_running_recognize(config=config, audio=audio)
        return operation.name
