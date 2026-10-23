import os
from google.cloud import speech_v1p1beta1 as speech
from google.api_core.exceptions import GoogleAPICallError
from typing import Optional, Dict, Any
import json


class SpeechClientConfig:
    def __init__(self, credentials_path: Optional[str] = None):
        self.credentials_path = credentials_path or os.environ.get(
            "GOOGLE_APPLICATION_CREDENTIALS"
        )

        if not self.credentials_path:
            raise ValueError(
                "Google Cloud credentials not found. "
                "Set GOOGLE_APPLICATION_CREDENTIALS environment variable or provide credentials_path."
            )

        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = self.credentials_path

    def validate_credentials(self) -> bool:
        try:
            with open(self.credentials_path, "r") as f:
                creds = json.load(f)
                required_fields = [
                    "type",
                    "project_id",
                    "private_key_id",
                    "private_key",
                    "client_email",
                ]
                return all(field in creds for field in required_fields)
        except (FileNotFoundError, json.JSONDecodeError):
            return False


class SpeechClientHelper:
    def __init__(self, config: SpeechClientConfig):
        self.config = config
        self._client = None

    @property
    def client(self) -> speech.SpeechClient:
        if self._client is None:
            self._client = speech.SpeechClient()
        return self._client

    def create_streaming_config(
        self,
        language_code: str = "en-US",
        sample_rate: int = 16000,
        enable_punctuation: bool = True,
        enable_word_offsets: bool = True,
        model: str = "latest_long",
        use_enhanced: bool = True,
        speech_contexts: Optional[list] = None,
    ) -> speech.StreamingRecognitionConfig:

        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=sample_rate,
            language_code=language_code,
            enable_automatic_punctuation=enable_punctuation,
            enable_word_time_offsets=enable_word_offsets,
            enable_word_confidence=True,
            model=model,
            use_enhanced=use_enhanced,
        )

        streaming_config = speech.StreamingRecognitionConfig(
            config=config,
            interim_results=True,
        )

        if speech_contexts:
            streaming_config.speech_contexts = speech_contexts

        return streaming_config

    def create_audio_requests(self, audio_generator):
        for audio_content in audio_generator:
            yield speech.StreamingRecognizeRequest(audio_content=audio_content)

    def process_streaming_response(self, responses, callback=None):
        for response in responses:
            if not response.results:
                continue

            for result in response.results:
                if not result.alternatives:
                    continue

                alternative = result.alternatives[0]

                processed_result = {
                    "transcript": alternative.transcript,
                    "is_final": result.is_final,
                    "confidence": alternative.confidence if result.is_final else None,
                    "stability": getattr(result, "stability", None),
                    "language_code": result.language_code
                    if hasattr(result, "language_code")
                    else None,
                    "result_end_time": result.result_end_time.total_seconds()
                    if hasattr(result, "result_end_time")
                    else None,
                }

                if alternative.words:
                    processed_result["words"] = [
                        {
                            "word": word.word,
                            "start_time": word.start_time.total_seconds(),
                            "end_time": word.end_time.total_seconds(),
                            "confidence": getattr(word, "confidence", None),
                        }
                        for word in alternative.words
                    ]

                if callback:
                    callback(processed_result)
                else:
                    yield processed_result

    def start_streaming_recognition(
        self, audio_generator, language_code: str = "en-US", **kwargs
    ) -> Any:

        streaming_config = self.create_streaming_config(
            language_code=language_code, **kwargs
        )
        requests = self.create_audio_requests(audio_generator)

        try:
            responses = self.client.streaming_recognize(streaming_config, requests)
            return self.process_streaming_response(responses)
        except GoogleAPICallError as e:
            raise Exception(f"Google Cloud Speech API error: {e}")


def get_speech_client(credentials_path: Optional[str] = None) -> SpeechClientHelper:
    config = SpeechClientConfig(credentials_path)
    return SpeechClientHelper(config)
