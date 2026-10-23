# [SAME-SCENARIO] stream_microphone.py

import asyncio
from google.cloud import speech_v1p1beta1 as speech

# Identify provider: Google Cloud Speech-to-Text


async def stream_microphone(sample_rate_hertz=16000, language_code="en-US"):
    client = speech.SpeechClient()
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=sample_rate_hertz,
        language_code=language_code,
        enable_automatic_punctuation=True,
    )
    streaming_config = speech.StreamingRecognitionConfig(
        config=config,
        interim_results=True,
    )
    # Helper to capture microphone audio asynchronously (implementation omitted for brevity)
    async for audio_chunk in capture_microphone():
        yield streaming_config, audio_chunk


# The capture_microphone coroutine should provide LINEAR16 audio data.
