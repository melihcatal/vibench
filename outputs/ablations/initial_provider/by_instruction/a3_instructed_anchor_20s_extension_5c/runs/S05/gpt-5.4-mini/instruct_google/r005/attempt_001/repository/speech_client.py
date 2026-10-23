import os
from dataclasses import dataclass
from typing import Optional

from google.api_core.client_options import ClientOptions
from google.cloud import speech_v1p1beta1 as speech


@dataclass
class SpeechConfig:
    language_code: str = "en-US"
    enable_punctuation: bool = True
    model: str = "latest_long"
    project_id: Optional[str] = None


def load_config() -> SpeechConfig:
    return SpeechConfig(
        language_code=os.getenv("GOOGLE_SPEECH_LANGUAGE_CODE", "en-US"),
        enable_punctuation=os.getenv("GOOGLE_SPEECH_ENABLE_PUNCTUATION", "true").lower() == "true",
        model=os.getenv("GOOGLE_SPEECH_MODEL", "latest_long"),
        project_id=os.getenv("GOOGLE_CLOUD_PROJECT"),
    )


def build_client() -> speech.SpeechClient:
    endpoint = os.getenv("GOOGLE_SPEECH_API_ENDPOINT")
    if endpoint:
        return speech.SpeechClient(client_options=ClientOptions(api_endpoint=endpoint))
    return speech.SpeechClient()


def recognition_config(config: SpeechConfig) -> speech.RecognitionConfig:
    return speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code=config.language_code,
        enable_automatic_punctuation=config.enable_punctuation,
        model=config.model,
        use_enhanced=True,
    )


def streaming_config(config: SpeechConfig) -> speech.StreamingRecognitionConfig:
    return speech.StreamingRecognitionConfig(
        config=recognition_config(config),
        interim_results=True,
        single_utterance=False,
    )
