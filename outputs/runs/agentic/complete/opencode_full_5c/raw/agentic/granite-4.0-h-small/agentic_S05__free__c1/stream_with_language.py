import json
from typing import AsyncGenerator

from google.cloud import speech_v1p1beta1 as speech
from speech_client import get_google_client

LANGUAGE_CODE = "es-ES"  # Example: Spanish
ENCODING = speech.RecognitionConfig.AudioEncoding.LINEAR16
SAMPLE_RATE = 16000


async def microphone_generator():
    # Placeholder for actual mic implementation - same as in stream_microphone.py
    # Implement or import real microphone stream here
    raise NotImplementedError


def start_streaming(client, language_code):
    config = speech.RecognitionConfig(
        encoding=ENCODING,
        sample_rate_hertz=SAMPLE_RATE,
        language_code=language_code,
        enable_automatic_punctuation=True,
    )
    streaming_config = speech.StreamingRecognitionConfig(
        config=config,
        interim_results=True,
    )
    return client.streaming_recognize(streaming_config, microphone_generator())


if __name__ == "__main__":
    client = get_google_client()
    responses = start_streaming(client, LANGUAGE_CODE)
    # Process responses as needed (e.g., using handle_stream_response from partial_results.py)
    try:
        for resp in responses:
            print(
                [
                    alt.transcript
                    for result in resp.results
                    for alt in result.alternatives
                ]
            )
    except KeyboardInterrupt:
        print("Stopped streaming.")
