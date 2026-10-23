import json
from typing import AsyncGenerator

from google.cloud.speech_v1p1beta1 import (
    StreamingRecognizeResponse,
    SpeechRecognitionResult,
    SpeechRecognitionAlternative,
)

from speech_client import get_google_client


def handle_stream_response(responses: AsyncGenerator[StreamingRecognizeResponse, None]):
    """Iterate through streaming responses and extract interim/final transcripts."""
    for response in responses:
        if not response.results:
            continue
        for result in response.results:
            if result.alternatives:
                alternative = result.alternatives[0]
                if result.is_final:
                    print(f"[FINAL] {alternative.transcript}")
                else:
                    # Interim result - show with confidence
                    print(
                        f"[INTERIM] {alternative.transcript} (confidence: {alternative.confidence:.2f})"
                    )
            else:
                print("[NO ALTERNATIVE]")


def stream_and_handle(client, streaming_config):
    """Start the streaming recognizer and feed it with microphone audio."""
    # The microphone_generator is defined in stream_microphone.py
    from stream_microphone import microphone_generator

    responses = client.streaming_recognize(streaming_config, microphone_generator())
    handle_stream_response(responses)


# Example entry point for quick testing
if __name__ == "__main__":
    client = get_google_client()
    config = client.recognize_config(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US",
        enable_automatic_punctuation=True,
    )
    stream_and_handle(client, config)
