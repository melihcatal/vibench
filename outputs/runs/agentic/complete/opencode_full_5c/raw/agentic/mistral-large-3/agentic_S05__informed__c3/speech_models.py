from google.cloud.speech_v1p1beta1 import types
from dataclasses import dataclass


@dataclass
class StreamingRecognitionConfig:
    """Configuration for streaming speech recognition."""

    language_code: str
    enable_automatic_punctuation: bool = True
    interim_results: bool = True
    model: str = "latest_long"

    def to_grpc(self):
        return types.RecognitionConfig(
            encoding=types.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=16000,
            language_code=self.language_code,
            enable_automatic_punctuation=self.enable_automatic_punctuation,
            model=self.model,
        )
