import os
from google.cloud import speech
from google.api_core.exceptions import GoogleAPICallError

class SpeechClient:
    """Provides a client for Google Cloud Speech-to-Text."""

    def __init__(self):
        # Initialize the Google Cloud Speech client. This assumes GOOGLE_APPLICATION_CREDENTIALS
        # environment variable is set or ADC is configured.
        self._client = speech.SpeechClient()

    def get_client(self):
        return self._client

    def create_streaming_config(self, config_params):
        """Creates a StreamingRecognitionConfig object."""
        recognition_config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding[config_params["encoding"]],
            sample_rate_hertz=config_params["sample_rate_hertz"],
            language_code=config_params["language_code"],
            enable_automatic_punctuation=config_params.get("enable_automatic_punctuation", False)
        )
        streaming_config = speech.StreamingRecognitionConfig(
            config=recognition_config,
            interim_results=True # Always enable interim results for streaming
        )
        return streaming_config

    def stream_recognize(self, streaming_config, audio_chunks_generator):
        """Yields streaming recognition responses."""
        requests = (speech.StreamingRecognizeRequest(audio_content=chunk) for chunk in audio_chunks_generator)
        try:
            for response in self._client.streaming_recognize(config=streaming_config, requests=requests):
                yield response
        except GoogleAPICallError as e:
            print(f"Google Cloud Speech API Error: {e}")
            raise
