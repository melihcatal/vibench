from dataclasses import dataclass
from typing import List, Optional

from google.cloud import speech_v2
from google.cloud.speech_v2 import types

@dataclass
class SpeechRecognitionChunk:
    transcript: str
    is_final: bool
    confidence: Optional[float] = None
    stability: Optional[float] = None
    language_code: Optional[str] = None

    @classmethod
    def from_speech_result(cls, result: types.StreamingRecognitionResult) -> Optional['SpeechRecognitionChunk']:
        """Normalizes a Google Cloud Speech-to-Text StreamingRecognitionResult to a SpeechRecognitionChunk."""
        if not result.alternatives:
            return None

        # Use the first alternative as the primary transcript
        first_alternative = result.alternatives[0]

        return cls(
            transcript=first_alternative.transcript,
            is_final=result.is_final,
            confidence=first_alternative.confidence if first_alternative.confidence > 0 else None,
            stability=result.stability if result.stability > 0 else None,
            language_code=result.language_code # Available in V2 results
        )

@dataclass
class StreamingRecognitionConfigParams:
    language_codes: List[str]
    sample_rate_hertz: int
    encoding: types.RecognitionConfig.AudioEncoding = types.RecognitionConfig.AudioEncoding.LINEAR16
    enable_automatic_punctuation: bool = True
    interim_results: bool = True
    model: str = "latest_long" # e.g., "latest_long", "latest_short", "telephony"

    def to_streaming_recognize_config(self) -> types.StreamingRecognitionConfig:
        config = types.RecognitionConfig(
            encoding=self.encoding,
            sample_rate_hertz=self.sample_rate_hertz,
            language_codes=self.language_codes,
            model=self.model,
            enable_automatic_punctuation=self.enable_automatic_punctuation,
        )
        return types.StreamingRecognitionConfig(
            config=config,
            interim_results=self.interim_results
        )


if __name__ == "__main__":
    print("--- Speech Models Helper --- ")

    # Example of creating a config
    config_params = StreamingRecognitionConfigParams(
        language_codes=["en-US"],
        sample_rate_hertz=16000,
        enable_automatic_punctuation=True
    )
    streaming_config = config_params.to_streaming_recognize_config()
    print(f"Generated StreamingRecognitionConfig: {streaming_config}")

    # Example of normalizing a mock result
    mock_speech_result = types.StreamingRecognitionResult(
        alternatives=[
            types.SpeechRecognitionAlternative(transcript="hello world", confidence=0.95)
        ],
        is_final=True,
        stability=0.99,
        language_code="en-US"
    )
    chunk = SpeechRecognitionChunk.from_speech_result(mock_speech_result)
    if chunk:
        print(f"Normalized chunk: {chunk}")

    mock_partial_result = types.StreamingRecognitionResult(
        alternatives=[
            types.SpeechRecognitionAlternative(transcript="hello wo", confidence=0.88)
        ],
        is_final=False,
        stability=0.75,
        language_code="en-US"
    )
    partial_chunk = SpeechRecognitionChunk.from_speech_result(mock_partial_result)
    if partial_chunk:
        print(f"Normalized partial chunk: {partial_chunk}")

