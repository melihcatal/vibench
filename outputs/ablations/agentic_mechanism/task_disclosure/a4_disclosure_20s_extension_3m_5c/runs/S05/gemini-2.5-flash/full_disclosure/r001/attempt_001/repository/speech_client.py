
import google.cloud.speech_v1p1beta1 as speech


class SpeechClient:
    """Provides local configuration and client helper utilities for Streaming Speech-to-Text."""

    def __init__(self, language_code: str = "en-US", sample_rate_hertz: int = 16000):
        self.client = speech.SpeechClient()
        self.config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=sample_rate_hertz,
            language_code=language_code,
        )
        self.streaming_config = speech.StreamingRecognitionConfig(
            config=self.config,
            interim_results=True,
        )

    def get_streaming_config(self):
        return self.streaming_config

    def stream_recognize(self, audio_chunks):
        """
        Sends audio chunks to the Google Cloud Speech-to-Text API and yields responses.
        """
        requests = (
            speech.StreamingRecognizeRequest(audio_content=chunk)
            for chunk in audio_chunks
        )
        responses = self.client.streaming_recognize(self.streaming_config, requests)
        return responses
