from dataclasses import dataclass
from typing import Iterator, Dict, Any

@dataclass
class RecognitionRequest:
    audio_chunks: Iterator[bytes]
    sample_rate_hz: int
    language_code: str
    enable_automatic_punctuation: bool = False

@dataclass
class SpeechRecognitionResult:
    text: str
    is_final: bool
    language_code: str = "en-US"

def normalize_response(response: Dict[str, Any]) -> SpeechRecognitionResult:
    # This is a placeholder for potential response normalization
    # In a real scenario, this would parse the provider's response format
    # For Google Cloud Speech-to-Text, the stream_microphone already handles basic parsing.
    # This function could be expanded to handle more complex scenarios or different providers.
    return SpeechRecognitionResult(
        text=response.get("text", ""),
        is_final=response.get("is_final", False),
        language_code=response.get("language_code", "en-US")
    )
