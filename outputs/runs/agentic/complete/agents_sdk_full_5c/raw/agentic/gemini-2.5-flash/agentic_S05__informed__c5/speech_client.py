from google.cloud import speech
import os

def get_speech_client() -> speech.SpeechClient:
    """Provides a configured Google Cloud Speech-to-Text client."""
    # Ensure GOOGLE_APPLICATION_CREDENTIALS is set for authentication
    if "GOOGLE_APPLICATION_CREDENTIALS" not in os.environ:
        print("Warning: GOOGLE_APPLICATION_CREDENTIALS environment variable not set.")
        print("Please ensure it points to your service account key file for Google Cloud Speech-to-Text.")
        print("Client initialization might fail or use default credentials if available.")
    
    return speech.SpeechClient()

def create_recognition_config(
    rate_hertz: int = 16000,
    language_code: str = "en-US",
    enable_automatic_punctuation: bool = True,
    enable_word_time_offsets: bool = False,
    encoding: speech.RecognitionConfig.AudioEncoding = speech.RecognitionConfig.AudioEncoding.LINEAR16,
) -> speech.RecognitionConfig:
    """Creates a Google Cloud Speech-to-Text RecognitionConfig."""
    return speech.RecognitionConfig(
        encoding=encoding,
        sample_rate_hertz=rate_hertz,
        language_code=language_code,
        enable_automatic_punctuation=enable_automatic_punctuation,
        enable_word_time_offsets=enable_word_time_offsets,
    )

def create_streaming_config(
    recognition_config: speech.RecognitionConfig,
    interim_results: bool = True,
) -> speech.StreamingRecognitionConfig:
    """Creates a Google Cloud Speech-to-Text StreamingRecognitionConfig."""
    return speech.StreamingRecognitionConfig(
        config=recognition_config,
        interim_results=interim_results,
    )
