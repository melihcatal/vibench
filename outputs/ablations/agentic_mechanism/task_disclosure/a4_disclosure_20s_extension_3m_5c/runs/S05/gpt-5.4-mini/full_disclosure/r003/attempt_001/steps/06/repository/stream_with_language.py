import os
from typing import AsyncIterator, Optional

from google.cloud import speech_v1 as speech


class StreamingSpeechRecognizer:
    def __init__(self, language_code: str = "en-US", enable_punctuation: bool = True):
        self.client = speech.SpeechClient()
        self.language_code = language_code
        self.enable_punctuation = enable_punctuation

    def _streaming_config(self) -> speech.StreamingRecognitionConfig:
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=int(os.getenv("SPEECH_SAMPLE_RATE", "16000")),
            language_code=self.language_code,
            enable_automatic_punctuation=self.enable_punctuation,
            model=os.getenv("GOOGLE_CLOUD_SPEECH_MODEL", "latest_long"),
        )
        return speech.StreamingRecognitionConfig(
            config=config,
            interim_results=True,
            single_utterance=False,
        )

    def recognize(self, audio_chunks: AsyncIterator[bytes]):
        requests = (
            speech.StreamingRecognizeRequest(audio_content=chunk)
            async for chunk in audio_chunks
        )
        return self.client.streaming_recognize(
            config=self._streaming_config(),
            requests=requests,
        )
