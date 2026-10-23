import os
from dataclasses import dataclass, field
from typing import Optional

from google.cloud.speech_v2 import SpeechClient
from google.api_core.client_options import ClientOptions


GOOGLE_CLOUD_SPEECH_ENDPOINT = "speech.googleapis.com"
GOOGLE_CLOUD_SPEECH_MODEL = "latest_long"
GOOGLE_CLOUD_SPEECH_LANGUAGE = "en-US"
GOOGLE_CLOUD_SPEECH_SAMPLE_RATE = 16000
GOOGLE_CLOUD_SPEECH_ENCODING = "LINEAR16"


@dataclass
class SpeechConfig:
    project_id: str = ""
    location: str = "global"
    model: str = GOOGLE_CLOUD_SPEECH_MODEL
    language_code: str = GOOGLE_CLOUD_SPEECH_LANGUAGE
    sample_rate_hertz: int = GOOGLE_CLOUD_SPEECH_SAMPLE_RATE
    encoding: str = GOOGLE_CLOUD_SPEECH_ENCODING
    enable_automatic_punctuation: bool = True
    enable_word_time_offsets: bool = True
    enable_word_confidence: bool = True
    max_alternatives: int = 1
    profanity_filter: bool = False
    enable_spoken_punctuation: bool = False
    audio_channel_count: int = 1
    credentials_path: Optional[str] = None
    api_endpoint: str = GOOGLE_CLOUD_SPEECH_ENDPOINT

    @classmethod
    def from_env(cls) -> "SpeechConfig":
        return cls(
            project_id=os.environ.get("GOOGLE_CLOUD_PROJECT", ""),
            location=os.environ.get("GOOGLE_CLOUD_LOCATION", "global"),
            model=os.environ.get("GOOGLE_SPEECH_MODEL", GOOGLE_CLOUD_SPEECH_MODEL),
            language_code=os.environ.get(
                "GOOGLE_SPEECH_LANGUAGE", GOOGLE_CLOUD_SPEECH_LANGUAGE
            ),
            sample_rate_hertz=int(
                os.environ.get(
                    "GOOGLE_SPEECH_SAMPLE_RATE", str(GOOGLE_CLOUD_SPEECH_SAMPLE_RATE)
                )
            ),
            encoding=os.environ.get(
                "GOOGLE_SPEECH_ENCODING", GOOGLE_CLOUD_SPEECH_ENCODING
            ),
            enable_automatic_punctuation=os.environ.get(
                "GOOGLE_SPEECH_PUNCTUATION", "true"
            ).lower()
            == "true",
            enable_word_time_offsets=os.environ.get(
                "GOOGLE_SPEECH_WORD_OFFSETS", "true"
            ).lower()
            == "true",
            enable_word_confidence=os.environ.get(
                "GOOGLE_SPEECH_WORD_CONFIDENCE", "true"
            ).lower()
            == "true",
            max_alternatives=int(os.environ.get("GOOGLE_SPEECH_MAX_ALTERNATIVES", "1")),
            profanity_filter=os.environ.get(
                "GOOGLE_SPEECH_PROFANITY_FILTER", "false"
            ).lower()
            == "true",
            enable_spoken_punctuation=os.environ.get(
                "GOOGLE_SPEECH_SPOKEN_PUNCTUATION", "false"
            ).lower()
            == "true",
            audio_channel_count=int(os.environ.get("GOOGLE_SPEECH_CHANNEL_COUNT", "1")),
            credentials_path=os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"),
            api_endpoint=os.environ.get(
                "GOOGLE_SPEECH_API_ENDPOINT", GOOGLE_CLOUD_SPEECH_ENDPOINT
            ),
        )

    @property
    def recognizer_path(self) -> str:
        return f"projects/{self.project_id}/locations/{self.location}/recognizers/_"

    @property
    def client_options(self) -> ClientOptions:
        return ClientOptions(api_endpoint=self.api_endpoint)


def create_speech_client(config: Optional[SpeechConfig] = None) -> SpeechClient:
    if config is None:
        config = SpeechConfig.from_env()
    return SpeechClient(client_options=config.client_options)


def build_recognition_config(config: SpeechConfig):
    from google.cloud.speech_v2.types import cloud_speech

    return cloud_speech.RecognitionConfig(
        explicit_decoding_config=cloud_speech.ExplicitDecodingConfig(
            encoding=cloud_speech.ExplicitDecodingConfig.AudioEncoding.LINEAR16
            if config.encoding == "LINEAR16"
            else cloud_speech.ExplicitDecodingConfig.AudioEncoding.ENCODING_UNSPECIFIED,
            sample_rate_hertz=config.sample_rate_hertz,
            audio_channel_count=config.audio_channel_count,
        ),
        language_codes=[config.language_code],
        model=config.model,
        features=cloud_speech.RecognitionFeatures(
            enable_automatic_punctuation=config.enable_automatic_punctuation,
            enable_word_time_offsets=config.enable_word_time_offsets,
            enable_word_confidence=config.enable_word_confidence,
            max_alternatives=config.max_alternatives,
            profanity_filter=config.profanity_filter,
            enable_spoken_punctuation=config.enable_spoken_punctuation,
        ),
    )
