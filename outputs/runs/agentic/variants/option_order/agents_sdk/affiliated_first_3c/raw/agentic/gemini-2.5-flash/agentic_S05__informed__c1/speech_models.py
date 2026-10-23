from typing import Optional, List
from dataclasses import dataclass
from google.cloud import speech_v1p1beta1 as speech
from google.cloud.speech_v1p1beta1 import enums

@dataclass
class StreamingRecognitionConfigParams:
    """Parameters for configuring streaming speech recognition."""
    encoding: enums.RecognitionConfig.AudioEncoding = enums.RecognitionConfig.AudioEncoding.LINEAR16
    sample_rate_hertz: int = 16000
    language_code: str = "en-US"
    enable_automatic_punctuation: bool = True
    interim_results: bool = True
    model: Optional[str] = None # e.g., "default", "command_and_search", "phone_call", "video"
    use_enhanced: Optional[bool] = None

    def to_streaming_recognition_config(self) -> speech.StreamingRecognitionConfig:
        """Converts the parameters to a Google Cloud `StreamingRecognitionConfig` object."""
        recognition_config = speech.RecognitionConfig(
            encoding=self.encoding,
            sample_rate_hertz=self.sample_rate_hertz,
            language_code=self.language_code,
            enable_automatic_punctuation=self.enable_automatic_punctuation,
            model=self.model,
            use_enhanced=self.use_enhanced,
        )
        return speech.StreamingRecognitionConfig(
            config=recognition_config,
            interim_results=self.interim_results,
        )

@dataclass
class TranscriptResult:
    """Represents a single transcript result from streaming recognition."""
    transcript: str
    is_final: bool
    confidence: Optional[float] = None
    language_code: Optional[str] = None

    @staticmethod
    def from_google_speech_result(result: speech.StreamingRecognitionResult) -> Optional['TranscriptResult']:
        """Normalizes a Google Cloud `StreamingRecognitionResult` to a `TranscriptResult`."""
        if not result.alternatives:
            return None
        
        # Take the first alternative (most likely)
        first_alternative = result.alternatives[0]
        return TranscriptResult(
            transcript=first_alternative.transcript,
            is_final=result.is_final,
            confidence=first_alternative.confidence if first_alternative.confidence > 0 else None,
            language_code=result.language_code, # available in some scenarios
        )


if __name__ == "__main__":
    print("Speech models and normalization helpers.")

    # Example usage of StreamingRecognitionConfigParams
    params = StreamingRecognitionConfigParams(language_code="es-ES", enable_automatic_punctuation=False)
    streaming_config = params.to_streaming_recognition_config()
    print(f"Config language code: {streaming_config.config.language_code}")
    print(f"Config punctuation enabled: {streaming_config.config.enable_automatic_punctuation}")

    # Example usage of TranscriptResult (mocking a Google Cloud Speech result)
    mock_alternative = speech.SpeechRecognitionAlternative(transcript="hello world", confidence=0.95)
    mock_result = speech.StreamingRecognitionResult(alternatives=[mock_alternative], is_final=True)
    
    normalized_result = TranscriptResult.from_google_speech_result(mock_result)
    if normalized_result:
        print(f"Normalized Transcript: {normalized_result.transcript}")
        print(f"Is Final: {normalized_result.is_final}")
        print(f"Confidence: {normalized_result.confidence}")
