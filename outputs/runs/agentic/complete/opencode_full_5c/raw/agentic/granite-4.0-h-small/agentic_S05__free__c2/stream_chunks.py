# [SAME-SCENARIO] stream_chunks.py

import asyncio
from google.cloud import speech_v1p1beta1 as speech

# Identify provider: Google Cloud Speech-to-Text


async def stream_chunks(audio_source, chunk_size=6400):
    client = speech.SpeechClient()
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US",
        enable_automatic_punctuation=True,
    )
    streaming_config = speech.StreamingRecognitionConfig(
        config=config, interim_results=True
    )
    # audio_source is an async iterable yielding bytes
    async for data in audio_source:
        yield streaming_config, data[:chunk_size]
