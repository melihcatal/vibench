import asyncio
import json

from google.cloud import speech_v1p1beta1 as speech
from google.cloud import translate_v2 as translate
from speech_models import extract_alternatives
from speech_client import get_google_client

# Configuration
TARGET_LANGUAGE = "fr"  # French


def translate_text(text: str) -> str:
    """Translate text using Google Cloud Translation API."""
    client = translate.Client()
    result = client.translate(text, target_language=TARGET_LANGUAGE)
    return result["translatedText"]


async def microphone_generator():
    # Same implementation as in stream_microphone.py
    raise NotImplementedError("Implement actual mic streaming")


def process_stream(client, config):
    """Stream audio, extract captions, translate, and print them."""
    responses = client.streaming_recognize(config, microphone_generator())
    for resp in responses:
        alternatives = extract_alternatives(resp)
        for alt in alternatives:
            caption = alt["transcript"]
            translation = translate_text(caption)
            print(f"[CAPTION] {caption} -> [TRANSLATION] {translation}")


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
    # Run in an event loop (example)
    asyncio.run(process_stream(client, config))


if __name__ == "__main__":
    main()
