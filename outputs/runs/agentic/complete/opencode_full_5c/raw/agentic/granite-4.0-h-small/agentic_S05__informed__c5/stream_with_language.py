import asyncio
from google.cloud import speech_v1 as speech

# Starts a streaming recognizer with explicit language, punctuation, and optional profanity filter configuration.
# Provider: Google Cloud Speech (service=Cloud Speech streaming)


def create_streaming_recognizer(language="en-US", enable_punctuation=True):
    """
    Returns a configured SpeechClient and RecognitionConfig for streaming.
    """
    client = speech.v1.SpeechClient()
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code=language,
        enable_automatic_punctuation=enable_punctuation,
    )
    streaming_config = speech.StreamingRecognitionConfig(
        config=config, interim_results=True
    )
    return client, config, streaming_config


async def start_stream(client, streaming_config, audio_iter):
    """Streams audio and yields results indefinitely."""
    request = speech.StreamingRecognizeRequest(streaming_config=streaming_config)
    async for audio in audio_iter:
        yield request.replace(audio_stream=audio)
