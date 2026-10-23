import os
from google.cloud import speech

def get_speech_client():
    """Returns an initialized Google Cloud SpeechClient."""
    # Google Cloud client libraries automatically use GOOGLE_APPLICATION_CREDENTIALS
    # environment variable for authentication.
    if "GOOGLE_APPLICATION_CREDENTIALS" not in os.environ:
        print("Warning: GOOGLE_APPLICATION_CREDENTIALS environment variable is not set.")
        print("Please ensure it points to your service account key file for proper authentication.")
    try:
        client = speech.SpeechClient()
        print("Google Cloud SpeechClient initialized.")
        return client
    except Exception as e:
        print(f"Error initializing Google Cloud SpeechClient: {e}")
        raise

def create_recognition_config(
    language_code: str = "en-US",
    sample_rate_hertz: int = 16000,
    enable_automatic_punctuation: bool = True,
    enable_word_time_offsets: bool = False,
) -> speech.RecognitionConfig:
    """Creates a Google Cloud Speech RecognitionConfig."""
    return speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=sample_rate_hertz,
        language_code=language_code,
        enable_automatic_punctuation=enable_automatic_punctuation,
        enable_word_time_offsets=enable_word_time_offsets,
    )

def create_streaming_recognition_config(
    config: speech.RecognitionConfig,
    interim_results: bool = True,
) -> speech.StreamingRecognitionConfig:
    """Creates a Google Cloud Speech StreamingRecognitionConfig."""
    return speech.StreamingRecognitionConfig(
        config=config,
        interim_results=interim_results,
    )

if __name__ == "__main__":
    # Example usage:
    try:
        client = get_speech_client()
        # You can now use the client in your application.
        print("SpeechClient obtained successfully.")

        rec_config = create_recognition_config(language_code="es-ES")
        print(f"Created recognition config for {rec_config.language_code}")

        stream_config = create_streaming_recognition_config(rec_config)
        print(f"Created streaming config with interim results: {stream_config.interim_results}")

    except Exception as e:
        print(f"An error occurred in speech_client.py example usage: {e}")
