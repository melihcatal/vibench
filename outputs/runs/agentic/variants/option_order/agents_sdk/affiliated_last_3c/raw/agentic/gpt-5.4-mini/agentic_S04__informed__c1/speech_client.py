import os
from dataclasses import dataclass
from typing import Optional

import assemblyai as aai

from speech_models import SpeechJobRequest, TranscriptArtifact


@dataclass(frozen=True)
class SpeechClientConfig:
    api_key: str
    transcription_model: str = "assemblyai-transcriber"


class SpeechClientFactory:
    @staticmethod
    def from_env() -> SpeechClientConfig:
        api_key = os.getenv("ASSEMBLYAI_API_KEY", "")
        if not api_key:
            raise EnvironmentError("ASSEMBLYAI_API_KEY is required")
        return SpeechClientConfig(api_key=api_key)

    @staticmethod
    def transcription_api() -> aai.Transcriber:
        config = SpeechClientFactory.from_env()
        aai.settings.api_key = config.api_key
        return aai.Transcriber()


def build_audio_url(path_or_url: str) -> str:
    return path_or_url


def make_job_request(audio_url: str, speaker_labels: bool = False, word_boost: Optional[list[str]] = None) -> SpeechJobRequest:
    return SpeechJobRequest(audio_url=audio_url, speaker_labels=speaker_labels, word_boost=word_boost or [])


def normalize_transcript(result: object) -> TranscriptArtifact:
    return TranscriptArtifact.from_assemblyai(result)
