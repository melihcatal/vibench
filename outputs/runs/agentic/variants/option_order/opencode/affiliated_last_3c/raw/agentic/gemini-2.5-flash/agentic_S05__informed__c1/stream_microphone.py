import os
import pyaudio
from google.cloud import speech_v1p1beta1 as speech
from speech_client import get_speech_client
from speech_models import StreamingRecognitionRequest, normalize_response


RATE = 16000
CHUNK = int(RATE / 10)  # 100ms chunks


def stream_microphone():
    """Streams microphone audio to Google Cloud Speech-to-Text and yields interim transcripts."""
    client = get_speech_client()

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=RATE,
        language_code="en-US",
    )
    streaming_config = speech.StreamingRecognitionConfig(
        config=config,
        interim_results=True,
    )

    # Setup audio input
    audio_interface = pyaudio.PyAudio()
    audio_stream = audio_interface.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK,
    )

    def request_generator():
        while True:
            chunk = audio_stream.read(CHUNK, exception_on_overflow=False)
            if not chunk:
                break
            yield StreamingRecognitionRequest(audio_content=chunk).audio_content

    requests = request_generator()
    responses = client.streaming_recognize(streaming_config, requests)

    for response in responses:
        yield normalize_response(response)
