from google.cloud.speech_v1p1beta1.types import (
    RecognitionConfig,
    StreamingRecognitionConfig,
    StreamingRecognitionResult,
    StreamingRecognizeRequest,
    RecognitionMetadata,
)

# Example placeholder for a custom request/response model if needed,
# currently using Google Cloud Speech-to-Text types directly.


class CustomStreamingResult:
    """A simplified result class for demonstration."""

    def __init__(self, transcript: str, is_final: bool, language_code: str = "en-US"):
        self.transcript = transcript
        self.is_final = is_final
        self.language_code = language_code

    def to_dict(self):
        return {
            "transcript": self.transcript,
            "is_final": self.is_final,
            "language_code": self.language_code,
        }
