import asyncio
import os
import io

from google.cloud import speech

# GOOGLE_APPLICATION_CREDENTIALS environment variable should be set


async def stream_microphone_audio():
    client = speech.SpeechClient()
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US",
    )
    streaming_config = speech.StreamingRecognitionConfig(
        config=config, interim_results=True
    )

    # This is a placeholder for microphone audio input
    # In a real scenario, you would get audio from a microphone
    # For demonstration, we simulate audio chunks
    async def generate_audio_chunks():
        # Simulate 1 second of silent audio for demonstration
        # A real microphone would provide actual audio bytes
        for _ in range(5):
            yield (
                b"\x00" * 32000
            )  # 16000 samples/sec * 2 bytes/sample = 32000 bytes/sec
            await asyncio.sleep(1)

    requests = (
        speech.StreamingRecognizeRequest(audio_content=chunk)
        for chunk in generate_audio_chunks()
    )

    responses = client.streaming_recognize(streaming_config, requests)

    for response in responses:
        if not response.results:
            continue

        result = response.results[0]
        if not result.alternatives:
            continue

        transcript = result.alternatives[0].transcript
        yield transcript
