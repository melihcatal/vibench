from google.cloud import speech
from typing import Dict, Any

def create_streaming_recognize_request(audio_content: bytes) -> speech.StreamingRecognizeRequest:
    """Creates a StreamingRecognizeRequest for Google Cloud Speech-to-Text."""
    return speech.StreamingRecognizeRequest(audio_content=audio_content)

def parse_streaming_recognize_response(response: speech.StreamingRecognizeResponse) -> Dict[str, Any]:
    """Parses a Google Cloud Speech-to-Text StreamingRecognizeResponse into a dictionary.

    Args:
        response: The StreamingRecognizeResponse object.

    Returns:
        A dictionary containing parsed transcription results.
        Example: {'is_final': True, 'transcript': 'Hello world.', 'confidence': 0.95}
    """
    if not response.results:
        return {"is_final": False, "transcript": "", "confidence": 0.0}

    result = response.results[0]
    if not result.alternatives:
        return {"is_final": False, "transcript": "", "confidence": 0.0}

    alternative = result.alternatives[0]
    return {
        "is_final": result.is_final,
        "transcript": alternative.transcript,
        "confidence": alternative.confidence,
        "stability": result.stability, # Stability is only present for interim results
    }

def create_recognition_config_dict(
    rate_hertz: int = 16000,
    language_code: str = "en-US",
    enable_automatic_punctuation: bool = True,
    encoding_enum: speech.RecognitionConfig.AudioEncoding = speech.RecognitionConfig.AudioEncoding.LINEAR16,
) -> Dict[str, Any]:
    """Creates a dictionary representation of RecognitionConfig for easier manipulation or logging."""
    return {
        "encoding": encoding_enum.name,
        "sample_rate_hertz": rate_hertz,
        "language_code": language_code,
        "enable_automatic_punctuation": enable_automatic_punctuation,
    }
