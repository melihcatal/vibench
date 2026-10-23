import os
from typing import Optional, Dict, Any
from google.cloud import speech
from google.api_core.client_options import ClientOptions
import json


class SpeechClientConfig:
    def __init__(
        self, credentials_path: Optional[str] = None, project_id: Optional[str] = None
    ):
        self.credentials_path = credentials_path
        self.project_id = project_id
        self._client = None

    def load_credentials(self):
        if self.credentials_path and os.path.exists(self.credentials_path):
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = self.credentials_path
        elif "GOOGLE_APPLICATION_CREDENTIALS" not in os.environ:
            raise ValueError(
                "Google Cloud credentials not found. Set GOOGLE_APPLICATION_CREDENTIALS environment variable."
            )

    def get_client(self) -> speech.SpeechClient:
        if self._client is None:
            self.load_credentials()

            client_options = None
            if self.project_id:
                client_options = ClientOptions(quota_project_id=self.project_id)

            self._client = speech.SpeechClient(client_options=client_options)

        return self._client

    def get_default_config(
        self, language_code: str = "en-US"
    ) -> speech.RecognitionConfig:
        return speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=16000,
            language_code=language_code,
            enable_automatic_punctuation=True,
            enable_word_time_offsets=True,
            enable_word_confidence=True,
            model="default",
        )

    def get_streaming_config(
        self, interim_results: bool = True
    ) -> speech.StreamingRecognitionConfig:
        config = self.get_default_config()
        return speech.StreamingRecognitionConfig(
            config=config,
            interim_results=interim_results,
        )


class AudioFormatHelper:
    @staticmethod
    def validate_audio_format(
        sample_rate: int, channels: int = 1, encoding: str = "LINEAR16"
    ) -> bool:
        valid_sample_rates = [8000, 16000, 24000, 32000, 44100, 48000]
        valid_encodings = ["LINEAR16", "FLAC", "MULAW", "AMR", "AMR_WB", "OGG_OPUS"]

        if sample_rate not in valid_sample_rates:
            raise ValueError(
                f"Invalid sample rate: {sample_rate}. Valid rates: {valid_sample_rates}"
            )

        if encoding not in valid_encodings:
            raise ValueError(
                f"Invalid encoding: {encoding}. Valid encodings: {valid_encodings}"
            )

        if channels not in [1, 2]:
            raise ValueError(f"Invalid channel count: {channels}. Must be 1 or 2.")

        return True

    @staticmethod
    def get_encoding_enum(encoding_str: str):
        encoding_map = {
            "LINEAR16": speech.RecognitionConfig.AudioEncoding.LINEAR16,
            "FLAC": speech.RecognitionConfig.AudioEncoding.FLAC,
            "MULAW": speech.RecognitionConfig.AudioEncoding.MULAW,
            "AMR": speech.RecognitionConfig.AudioEncoding.AMR,
            "AMR_WB": speech.RecognitionConfig.AudioEncoding.AMR_WB,
            "OGG_OPUS": speech.RecognitionConfig.AudioEncoding.OGG_OPUS,
        }

        if encoding_str not in encoding_map:
            raise ValueError(f"Unsupported encoding: {encoding_str}")

        return encoding_map[encoding_str]


class ClientFactory:
    _instances = {}

    @classmethod
    def get_or_create_client(
        cls, credentials_path: Optional[str] = None, project_id: Optional[str] = None
    ) -> speech.SpeechClient:
        key = f"{credentials_path}:{project_id}"

        if key not in cls._instances:
            config = SpeechClientConfig(credentials_path, project_id)
            cls._instances[key] = config.get_client()

        return cls._instances[key]

    @classmethod
    def create_streaming_client(
        cls,
        language_code: str = "en-US",
        interim_results: bool = True,
        credentials_path: Optional[str] = None,
    ) -> Dict[str, Any]:
        client = cls.get_or_create_client(credentials_path)
        config = SpeechClientConfig(credentials_path)

        recognition_config = config.get_default_config(language_code)
        streaming_config = speech.StreamingRecognitionConfig(
            config=recognition_config,
            interim_results=interim_results,
        )

        return {
            "client": client,
            "recognition_config": recognition_config,
            "streaming_config": streaming_config,
        }


def load_config_from_file(config_path: str) -> Dict[str, Any]:
    with open(config_path, "r") as f:
        config = json.load(f)

    required_fields = ["language_code", "sample_rate"]
    for field in required_fields:
        if field not in config:
            raise ValueError(f"Missing required field in config: {field}")

    return config
