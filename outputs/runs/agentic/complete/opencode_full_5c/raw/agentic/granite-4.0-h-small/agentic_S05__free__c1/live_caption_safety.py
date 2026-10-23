import asyncio
import json

from google.cloud import speech_v1p1beta1 as speech
from speech_models import extract_alternatives
from speech_client import get_google_client

# Placeholder for unsafe content detection (e.g., Perspective API, custom filter)
from safety_filter import is_unsafe


async def microphone_generator():
    # Same as in stream_microphone.py (implement actual mic streaming)
    raise NotImplementedError


def safety_check_stream(client, config):
    """Stream audio, capture transcripts, and flag unsafe content."""
    responses = client.streaming_recognize(config, microphone_generator())
    for resp in responses:
        alternatives = extract_alternatives(resp)
        for alt in alternatives:
            text = alt["transcript"]
            if is_unsafe(text):
                print(f"[ALERT] Unsafe content detected: {text[:60]}...")
            else:
                print(f"[SAFE] {text}")


def main():
    client = get_google_client()
    config = speech.StreamingRecognitionConfig(
        config=speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=16000,
            language_code="en-US",
            enable_automatic_punctuation=True,
        ),
        interim_results=True,
    )
    asyncio.run(safety_check_stream(client, config))


if __name__ == "__main__":
    main()
