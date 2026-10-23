# [HELPER] speech_models.py
# Definition of request, response and normalization helpers for Google Speech Streaming API
from typing import Dict, Any, List
from google.cloud.speech_v1p1beta1 import types as speech_types
from google.cloud.speech_v1p1beta1 import enums

# Provider identifier
PROVIDER = "google"

### Request building helpers ###

def build_streaming_recognition_request(
    audio_chunk: bytes,
    config: speech_types.RecognitionConfig,
    config_class=speech_types.StreamingRecognitionConfig,
) -> speech_types.StreamingRecognizeRequest:
    """Create a StreamingRecognizeRequest containing the audio chunk and config."""
    return speech_types.StreamingRecognizeRequest(
        streaming_config=config_class(
            config=config, single_utterance=False, interim_results=True
        ),
        audio=types.RecognitionAudio(audio_source=speech_types.RecognitionAudio(audio=audio_chunk)),
    )

### Response parsing helpers ###

def parse_interim_response(response:
    speech_types.StreamingRecognizeResponse) -> List[str]:
    """Extract interim transcript strings from a response."""
    results: List[str] = []
    for result in response.results:
        if not result.alternatives:
            continue
        transcript = result.alternatives[0].transcript
        if result.is_final:
            results.append(transcript)
        else:
            results.append(transcript)
    return results

### Normalization helpers ###

def normalize_transcript(text: str) -> str:
    """Lowercase and strip leading/trailing whitespace."""
    return text.strip().lower()

if __name__ == "__main__":
    config = parse_interim_response(speech_types.StreamingRecognizeResponse())
    print("Parsed empty response yields:", config)
    norm = normalize_transcript("  Hello, World!  ")
    print("Normalized text:", norm)