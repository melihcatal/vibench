import os
from google.cloud import speech_v1p1beta1 as speech
from google.cloud.speech_v1p1beta1 import types
from typing import AsyncIterable, AsyncGenerator


class SpeechClient:
    """Provides local configuration and client helper utilities for Google Cloud Speech-to-Text."""

    def __init__(self):
        self._client = None

    def get_client(self) -> speech.SpeechClient:
        """Initializes and returns the Google Cloud Speech client."""
        if not self._client:
            self._client = speech.SpeechClient()
        return self._client

    async def streaming_recognize(
        self,
        config: types.StreamingRecognitionConfig,
        requests: AsyncIterable[types.StreamingRecognizeRequest],
    ) -> AsyncGenerator[types.StreamingRecognizeResponse, None]:
        """Performs streaming recognition with the provided config and requests."""
        client = self.get_client()
        streaming_config = types.StreamingRecognitionConfig(
            config=config.config,
            streaming_features=config.streaming_features,
        )
        response_iterator = client.streaming_recognize(
            request_iterator=requests, config=streaming_config
        )
        for response in response_iterator:
            yield response


def get_speech_client() -> SpeechClient:
    """Returns a singleton instance of SpeechClient."""
    return SpeechClient()
