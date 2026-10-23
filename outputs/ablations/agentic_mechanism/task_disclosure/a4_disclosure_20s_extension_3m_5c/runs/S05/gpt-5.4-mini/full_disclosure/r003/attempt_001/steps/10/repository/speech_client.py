import os
from dataclasses import dataclass
from typing import Optional

from google.cloud import speech_v1 as speech


DEFAULT_SAMPLE_RATE = int(os.getenv("SPEECH_SAMPLE_RATE", "16000"))
DEFAULT_LANGUAGE_CODE = os.getenv("SPEECH_LANGUAGE_CODE", "en-US")
DEFAULT_MODEL = os.getenv("GOOGLE_CLOUD_SPEECH_MODEL", "latest_long")
DEFAULT_ENABLE_PUNCTUATION = os.getenv("SPEECH_ENABLE_PUNCTUATION", "true").lower() not in {"0", "false", "no"}


@dataclass
class SpeechClientConfig:
    sample_rate_hertz: int = DEFAULT_SAMPLE_RATE
    language_code: str = DEFAULT_LANGUAGE_CODE
    model: str = DEFAULT_MODEL
    enable_automatic_punctuation: bool = DEFAULT_ENABLE_PUNCTUATION
    interim_results: bool = True
    single_utterance: bool = False


def get_speech_client() -> speech.SpeechClient:
    return speech.SpeechClient()


def get_streaming_recognition_config(
    language_code: Optional[str] = None,
    enable_punctuation: Optional[bool] = None,
    sample_rate_hertz: Optional[int] = None,
    model: Optional[str] = None,
) -> speech.StreamingRecognitionConfig:
    config = SpeechClientConfig(
        sample_rate_hertz=sample_rate_hertz if sample_rate_hertz is not None else DEFAULT_SAMPLE_RATE,
        language_code=language_code if language_code is not None else DEFAULT_LANGUAGE_CODE,
        model=model if model is not None else DEFAULT_MODEL,
        enable_automatic_punctuation=enable_punctuation if enable_punctuation is not None else DEFAULT_ENABLE_PUNCTUATION,
    )
    recognition_config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=config.sample_rate_hertz,
        language_code=config.language_code,
        enable_automatic_punctuation=config.enable_automatic_punctuation,
        model=config.model,
    )
    return speech.StreamingRecognitionConfig(
        config=recognition_config,
        interim_results=config.interim_results,
        single_utterance=config.single_utterance,
    )


def make_streaming_request(chunk: bytes) -> speech.StreamingRecognizeRequest:
    return speech.StreamingRecognizeRequest(audio_content=chunk)
