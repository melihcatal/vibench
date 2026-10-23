from dataclasses import dataclass

# Define common audio encoding and sample rate for consistency
DEFAULT_AUDIO_ENCODING = "LINEAR16"
DEFAULT_SAMPLE_RATE_HERTZ = 16000
DEFAULT_LANGUAGE_CODE = "en-US"

@dataclass
class TranscriptResult:
    transcript: str
    is_final: bool
    confidence: float = 0.0

@dataclass
class RecognitionSettings:
    sample_rate_hertz: int = DEFAULT_SAMPLE_RATE_HERTZ
    language_code: str = DEFAULT_LANGUAGE_CODE
    interim_results: bool = True
    enable_automatic_punctuation: bool = True
    model: str = "default" # e.g., "default", "command_and_search", "medical", "phone_call"

# You might add utility functions here for normalizing responses from the Speech-to-Text API
# or preparing custom request objects if the SDK's aren't sufficient directly.

def normalize_speech_response(response) -> list[TranscriptResult]:
    """Normalizes a Google Cloud Speech-to-Text streaming response into TranscriptResult objects."""
    results = []
    if response.results:
        for result in response.results:
            if result.alternatives:
                best_alternative = result.alternatives[0]
                results.append(
                    TranscriptResult(
                        transcript=best_alternative.transcript,
                        is_final=result.is_final,
                        confidence=best_alternative.confidence,
                    )
                )
    return results

