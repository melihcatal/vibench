import os
from dataclasses import dataclass, field
from typing import Optional

from google.cloud import speech_v2
from google.api_core.client_options import ClientOptions


@dataclass
class SpeechConfig:
    project_id: str = field(
        default_factory=lambda: os.getenv("GOOGLE_CLOUD_PROJECT", "")
    )
    location: str = field(
        default_factory=lambda: os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
    )
    credentials_path: Optional[str] = field(
        default_factory=lambda: os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    )
    sample_rate_hertz: int = 16000
    audio_encoding: str = "LINEAR16"
    language_code: str = "en-US"
    enable_automatic_punctuation: bool = True
    enable_word_time_offsets: bool = True
    model: str = "latest_long"
    profanity_filter: bool = False
    max_alternatives: int = 1

    @property
    def recognizer_path(self) -> str:
        return f"projects/{self.project_id}/locations/{self.location}/recognizers/_"

    @property
    def client_options(self) -> ClientOptions:
        host = f"speech.{self.location}.googleapis.com"
        return ClientOptions(api_endpoint=host)


def build_speech_client(config: SpeechConfig) -> speech_v2.SpeechClient:
    kwargs = {"client_options": config.client_options}
    if config.credentials_path:
        kwargs["credentials"] = config.credentials_path
    return speech_v2.SpeechClient(**kwargs)


def build_recognition_config(config: SpeechConfig) -> speech_v2.RecognitionConfig:
    encoding_map = {
        "LINEAR16": speech_v2.RecognitionConfig.AudioEncoding.LINEAR16,
        "MP3": speech_v2.RecognitionConfig.AudioEncoding.MP3,
        "OGG_OPUS": speech_v2.RecognitionConfig.AudioEncoding.OGG_OPUS,
        "MULAW": speech_v2.RecognitionConfig.AudioEncoding.MULAW,
        "AMR": speech_v2.RecognitionConfig.AudioEncoding.AMR,
        "AMR_WB": speech_v2.RecognitionConfig.AudioEncoding.AMR_WB,
        "FLAC": speech_v2.RecognitionConfig.AudioEncoding.FLAC,
    }
    return speech_v2.RecognitionConfig(
        auto_decoding_config=speech_v2.AutoDetectDecodingConfig(),
        language_codes=[config.language_code],
        model=config.model,
        features=speech_v2.RecognitionFeatures(
            enable_automatic_punctuation=config.enable_automatic_punctuation,
            enable_word_time_offsets=config.enable_word_time_offsets,
            profanity_filter=config.profanity_filter,
        ),
        explicit_decoding_config=speech_v2.ExplicitDecodingConfig(
            encoding=encoding_map.get(
                config.audio_encoding,
                speech_v2.RecognitionConfig.AudioEncoding.LINEAR16,
            ),
            sample_rate_hertz=config.sample_rate_hertz,
            audio_channel_count=1,
        ),
    )
