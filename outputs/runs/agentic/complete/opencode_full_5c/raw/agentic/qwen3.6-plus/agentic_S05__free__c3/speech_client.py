import os
import json
from typing import Optional, Dict, Any
from google.cloud import speech_v1p1beta1 as speech
from google.oauth2 import service_account
from google.api_core.client_options import ClientOptions


GOOGLE_SPEECH_API_ENDPOINT = "speech.googleapis.com"
DEFAULT_MODEL = "latest_long"
DEFAULT_LANGUAGE_CODE = "en-US"
DEFAULT_SAMPLE_RATE = 16000


class SpeechClientConfig:
    def __init__(
        self,
        credentials_path: Optional[str] = None,
        project_id: Optional[str] = None,
        api_endpoint: str = GOOGLE_SPEECH_API_ENDPOINT,
        timeout: float = 300.0,
    ):
        self.credentials_path = credentials_path or os.environ.get(
            "GOOGLE_APPLICATION_CREDENTIALS"
        )
        self.project_id = project_id or os.environ.get("GOOGLE_CLOUD_PROJECT")
        self.api_endpoint = api_endpoint
        self.timeout = timeout

    def get_credentials(self):
        if self.credentials_path:
            return service_account.Credentials.from_service_account_file(
                self.credentials_path,
                scopes=["https://www.googleapis.com/auth/cloud-platform"],
            )
        return None

    def get_client_options(self):
        return ClientOptions(api_endpoint=f"https://{self.api_endpoint}")


def create_speech_client(
    config: Optional[SpeechClientConfig] = None,
) -> speech.SpeechClient:
    if config is None:
        config = SpeechClientConfig()

    credentials = config.get_credentials()
    client_options = config.get_client_options()

    if credentials:
        return speech.SpeechClient(
            credentials=credentials,
            client_options=client_options,
        )
    return speech.SpeechClient(client_options=client_options)


def load_config_from_env() -> SpeechClientConfig:
    return SpeechClientConfig(
        credentials_path=os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"),
        project_id=os.environ.get("GOOGLE_CLOUD_PROJECT"),
        api_endpoint=os.environ.get(
            "GOOGLE_SPEECH_API_ENDPOINT", GOOGLE_SPEECH_API_ENDPOINT
        ),
        timeout=float(os.environ.get("GOOGLE_SPEECH_TIMEOUT", "300")),
    )


def load_config_from_file(config_path: str) -> SpeechClientConfig:
    with open(config_path, "r") as f:
        data = json.load(f)
    return SpeechClientConfig(
        credentials_path=data.get("credentials_path"),
        project_id=data.get("project_id"),
        api_endpoint=data.get("api_endpoint", GOOGLE_SPEECH_API_ENDPOINT),
        timeout=data.get("timeout", 300.0),
    )


def get_default_recognition_config(
    language_code: str = DEFAULT_LANGUAGE_CODE,
    model: str = DEFAULT_MODEL,
    sample_rate: int = DEFAULT_SAMPLE_RATE,
    enable_automatic_punctuation: bool = True,
    enable_word_time_offsets: bool = True,
    max_alternatives: int = 1,
) -> speech.RecognitionConfig:
    return speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=sample_rate,
        language_code=language_code,
        model=model,
        enable_automatic_punctuation=enable_automatic_punctuation,
        enable_word_time_offsets=enable_word_time_offsets,
        max_alternatives=max_alternatives,
    )


def get_streaming_config(
    recognition_config: speech.RecognitionConfig,
    interim_results: bool = True,
    single_utterance: bool = False,
) -> speech.StreamingRecognitionConfig:
    return speech.StreamingRecognitionConfig(
        config=recognition_config,
        interim_results=interim_results,
        single_utterance=single_utterance,
    )
