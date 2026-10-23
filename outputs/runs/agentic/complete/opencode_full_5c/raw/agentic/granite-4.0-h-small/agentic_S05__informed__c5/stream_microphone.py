import asyncio
from google.cloud import speech_v1 as speech

# This file streams microphone audio and yields interim transcripts using Google Cloud Speech-to-Text streaming.
# Provider: Google Cloud Speech (service=Cloud Speech streaming)


def recognize_microphone(**kwargs):
    """Configure and start microphone streaming recognizer yielding interim results."""
    client = (
        speech.v1.SpeechClient()
    )  # Authenticates with GOOGLE_APPLICATION_CREDENTIALS
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US",
        enable_automatic_punctuation=True,
    )
    streaming_config = speech.StreamingRecognitionConfig(
        config=config, interim_results=True
    )
    request = speech.StreamingRecognizeRequest(streaming_config=streaming_config)
    mic_stream = speech.MicrophoneStream(**kwargs)  # custom wrapper
    data = mic_stream.stream()
    for audio in data:
        yield request.replace(audio_stream=b"".join(audio))
