from google.cloud import speech

def parse_streaming_response(response: speech.StreamingRecognizeResponse):
    """Parses a Google Cloud Speech-to-Text streaming response."""
    if not response.results:
        return None, None, False

    result = response.results[0]
    if not result.alternatives:
        return None, None, False

    transcript = result.alternatives[0].transcript
    return transcript, result.stability, result.is_final

def create_recognition_config(
    sampling_rate: int = 16000,
    language_code: str = "en-US",
    enable_automatic_punctuation: bool = True,
) -> speech.RecognitionConfig:
    """Defines a Google Cloud Speech-to-Text recognition configuration."""
    return speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=sampling_rate,
        language_code=language_code,
        enable_automatic_punctuation=enable_automatic_punctuation,
    )
