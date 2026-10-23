
import os
import io

from google.cloud import speech_v1p1beta1 as speech
from google.cloud.speech_v1p1beta1 import enums
from google.cloud.speech_v1p1beta1 import types

def stream_with_language(
    language_code: str = "en-US",
    enable_automatic_punctuation: bool = True,
):
    """Streams audio to the Google Cloud Speech-to-Text API with specified
    language and punctuation settings.
    """

    client = speech.SpeechClient()

    # Configure recognition settings
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code=language_code,
        enable_automatic_punctuation=enable_automatic_punctuation,
    )
    streaming_config = types.StreamingRecognitionConfig(
        config=config,
        interim_results=False,
    )

    # Simulate audio input for demonstration purposes
    # In a real application, this would come from a microphone or audio file
    # For simplicity, we'll use a short hardcoded audio content.
    # Replace with actual audio input for a functional example.
    audio_content = b"Hello Google Cloud Speech to Text API"

    requests = [types.StreamingRecognizeRequest(audio_content=audio_content)]

    responses = client.streaming_recognize(streaming_config, requests)

    print(f"Streaming recognition with language_code={language_code} and "
          f"enable_automatic_punctuation={enable_automatic_punctuation}:")

    for response in responses:
        # Once the transcription has settled, the first result will contain the
        # IsFinal flag. The other results will be interim.
        for result in response.results:
            print(f"Finished: {result.is_final}")
            print(f"Stability: {result.stability}")
            alternatives = result.alternatives
            for alternative in alternatives:
                print(f"Confidence: {alternative.confidence}")
                print(f"Transcript: {alternative.transcript}")

if __name__ == "__main__":
    # Example usage:
    # Set GOOGLE_APPLICATION_CREDENTIALS environment variable
    # e.g., export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/keyfile.json"

    # Default settings (English, with punctuation)
    print("--- Running with default settings (en-US, punctuation enabled) ---")
    stream_with_language()

    print("
--- Running with Spanish language, no punctuation ---")
    stream_with_language(language_code="es-ES", enable_automatic_punctuation=False)
