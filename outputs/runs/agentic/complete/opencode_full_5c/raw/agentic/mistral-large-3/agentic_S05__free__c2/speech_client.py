from google.cloud import speech_v1p1beta1 as speech
from google.api_core.client_options import ClientOptions
from typing import Optional
import os


class SpeechClient:
    def __init__(self, api_key: Optional[str] = None, region: Optional[str] = None):
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        self.region = region or os.getenv("GOOGLE_REGION", "us-central1")
        client_options = ClientOptions(
            api_key=self.api_key,
            quota_project_id=os.getenv("GOOGLE_PROJECT_ID"),
        )
        self.client = speech.SpeechClient(client_options=client_options)

    def get_client(self) -> speech.SpeechClient:
        return self.client

    def get_config(
        self,
        language_code: str = "en-US",
        enable_punctuation: bool = True,
        model: str = "latest_long",
    ) -> speech.RecognitionConfig:
        return speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=16000,
            language_code=language_code,
            enable_automatic_punctuation=enable_punctuation,
            model=model,
        )

    def get_streaming_config(
        self, config: speech.RecognitionConfig, interim_results: bool = True
    ) -> speech.StreamingRecognitionConfig:
        return speech.StreamingRecognitionConfig(
            config=config, interim_results=interim_results
        )
