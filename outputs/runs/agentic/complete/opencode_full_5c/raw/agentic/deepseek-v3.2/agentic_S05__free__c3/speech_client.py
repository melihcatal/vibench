import os
from typing import Optional, Dict, Any
from google.cloud import speech_v1p1beta1 as speech
from google.api_core.client_options import ClientOptions
import json


class SpeechClientConfig:
    def __init__(
        self, credentials_path: Optional[str] = None, project_id: Optional[str] = None
    ):
        self.credentials_path = credentials_path
        self.project_id = project_id
        self._load_environment()

    def _load_environment(self):
        if not self.credentials_path:
            self.credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

        if not self.project_id:
            self.project_id = os.getenv("GOOGLE_CLOUD_PROJECT")

    def get_client_options(self) -> ClientOptions:
        options = ClientOptions()

        if self.project_id:
            options.quota_project_id = self.project_id

        return options

    def validate(self) -> bool:
        if not self.credentials_path or not os.path.exists(self.credentials_path):
            return False

        if not self.project_id:
            return False

        return True

    def to_dict(self) -> Dict[str, Any]:
        return {
            "credentials_path": self.credentials_path,
            "project_id": self.project_id,
            "is_valid": self.validate(),
        }


class SpeechClientHelper:
    def __init__(self, config: Optional[SpeechClientConfig] = None):
        self.config = config or SpeechClientConfig()

        if not self.config.validate():
            raise ValueError("Invalid Google Cloud Speech configuration")

        self.client = speech.SpeechClient(
            client_options=self.config.get_client_options()
        )

    def create_recognition_config(
        self,
        language_code: str = "en-US",
        sample_rate: int = 16000,
        enable_punctuation: bool = True,
        enable_word_confidence: bool = True,
        enable_word_time_offsets: bool = True,
        model: str = "default",
        use_enhanced: bool = False,
        audio_channel_count: int = 1,
    ) -> speech.RecognitionConfig:

        return speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=sample_rate,
            language_code=language_code,
            enable_automatic_punctuation=enable_punctuation,
            enable_word_confidence=enable_word_confidence,
            enable_word_time_offsets=enable_word_time_offsets,
            model=model,
            use_enhanced=use_enhanced,
            audio_channel_count=audio_channel_count,
        )

    def create_streaming_config(
        self,
        recognition_config: speech.RecognitionConfig,
        interim_results: bool = True,
        single_utterance: bool = False,
    ) -> speech.StreamingRecognitionConfig:

        return speech.StreamingRecognitionConfig(
            config=recognition_config,
            interim_results=interim_results,
            single_utterance=single_utterance,
        )

    def get_supported_languages(self) -> list:
        return [
            "en-US",
            "en-GB",
            "es-ES",
            "fr-FR",
            "de-DE",
            "it-IT",
            "ja-JP",
            "ko-KR",
            "zh-CN",
            "zh-TW",
            "pt-BR",
            "ru-RU",
            "nl-NL",
            "ar-SA",
            "hi-IN",
        ]

    def get_available_models(self) -> list:
        return ["default", "video", "phone_call", "command_and_search"]

    @staticmethod
    def load_config_from_file(config_path: str) -> SpeechClientConfig:
        with open(config_path, "r") as f:
            config_data = json.load(f)

        return SpeechClientConfig(
            credentials_path=config_data.get("credentials_path"),
            project_id=config_data.get("project_id"),
        )

    @staticmethod
    def save_config_to_file(config: SpeechClientConfig, config_path: str):
        config_dict = config.to_dict()
        with open(config_path, "w") as f:
            json.dump(config_dict, f, indent=2)


def get_speech_client(config_path: Optional[str] = None) -> speech.SpeechClient:
    if config_path:
        config = SpeechClientHelper.load_config_from_file(config_path)
    else:
        config = SpeechClientConfig()

    helper = SpeechClientHelper(config)
    return helper.client


def create_default_streaming_config(
    language_code: str = "en-US",
) -> speech.StreamingRecognitionConfig:
    helper = SpeechClientHelper()

    recognition_config = helper.create_recognition_config(
        language_code=language_code,
        enable_punctuation=True,
        enable_word_confidence=True,
        enable_word_time_offsets=True,
    )

    return helper.create_streaming_config(
        recognition_config, interim_results=True, single_utterance=False
    )
