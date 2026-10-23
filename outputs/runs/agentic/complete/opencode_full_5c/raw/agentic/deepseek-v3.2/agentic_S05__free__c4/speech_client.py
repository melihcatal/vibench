import os
from typing import Optional, Dict, Any
from google.cloud import speech_v1p1beta1 as speech
from google.api_core import client_options


class SpeechClientConfig:
    def __init__(
        self, credentials_path: Optional[str] = None, project_id: Optional[str] = None
    ):
        self.credentials_path = credentials_path
        self.project_id = project_id
        self._configure_environment()

    def _configure_environment(self):
        if self.credentials_path and os.path.exists(self.credentials_path):
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = self.credentials_path

    def get_client_options(self) -> Optional[client_options.ClientOptions]:
        if self.project_id:
            return client_options.ClientOptions(quota_project_id=self.project_id)
        return None


class SpeechClientHelper:
    def __init__(self, config: Optional[SpeechClientConfig] = None):
        self.config = config or SpeechClientConfig()
        self.client_options = self.config.get_client_options()
        self.client = self._create_client()

    def _create_client(self) -> speech.SpeechClient:
        if self.client_options:
            return speech.SpeechClient(client_options=self.client_options)
        return speech.SpeechClient()

    def get_default_config(self) -> speech.RecognitionConfig:
        return speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=16000,
            language_code="en-US",
            enable_automatic_punctuation=True,
            model="latest_long",
            use_enhanced=True,
        )

    def get_streaming_config(
        self, interim_results: bool = True
    ) -> speech.StreamingRecognitionConfig:
        config = self.get_default_config()
        return speech.StreamingRecognitionConfig(
            config=config,
            interim_results=interim_results,
        )

    def create_recognition_audio(
        self, content: bytes, uri: Optional[str] = None
    ) -> speech.RecognitionAudio:
        audio = speech.RecognitionAudio()
        if uri:
            audio.uri = uri
        else:
            audio.content = content
        return audio

    def create_streaming_request(
        self, audio_chunk: bytes
    ) -> speech.StreamingRecognizeRequest:
        return speech.StreamingRecognizeRequest(audio_content=audio_chunk)

    def batch_recognize(
        self, audio_content: bytes, config: Optional[speech.RecognitionConfig] = None
    ) -> speech.RecognizeResponse:
        if config is None:
            config = self.get_default_config()

        audio = self.create_recognition_audio(audio_content)
        response = self.client.recognize(config=config, audio=audio)
        return response

    def long_running_recognize(
        self, audio_uri: str, config: Optional[speech.RecognitionConfig] = None
    ) -> speech.LongRunningRecognizeResponse:
        if config is None:
            config = self.get_default_config()

        audio = self.create_recognition_audio(b"", uri=audio_uri)
        operation = self.client.long_running_recognize(config=config, audio=audio)
        return operation.result()

    @staticmethod
    def extract_transcripts(response: speech.RecognizeResponse) -> list:
        transcripts = []
        for result in response.results:
            if result.alternatives:
                transcripts.append(result.alternatives[0].transcript)
        return transcripts

    @staticmethod
    def extract_streaming_transcripts(streaming_response) -> list:
        transcripts = []
        for response in streaming_response:
            for result in response.results:
                if result.alternatives:
                    transcript = result.alternatives[0].transcript
                    is_final = result.is_final
                    transcripts.append((transcript, is_final))
        return transcripts
