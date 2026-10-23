import os
import pyaudio
import time
from google.cloud import speech_v1p1beta1 as speech
from google.cloud.speech_v1p1beta1 import enums
from google.cloud.speech_v1p1beta1 import types

from speech_client import get_speech_client, create_streaming_config

# Audio recording parameters
RATE = 16000
CHUNK = int(RATE / 10)  # 100ms chunks

def stream_microphone_audio():
    """Streams audio from the microphone to a generator."""
    audio_interface = pyaudio.PyAudio()
    audio_stream = audio_interface.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK,
    )

    print("Listening...")
    try:
        while True:
            data = audio_stream.read(CHUNK, exception_on_overflow=False)
            if data:
                yield data
            else:
                break
    except KeyboardInterrupt:
        pass
    finally:
        audio_stream.stop_stream()
        audio_stream.close()
        audio_interface.terminate()
        print("Stopped listening.")


def recognize_microphone_stream(language_code: str = "en-US", enable_punctuation: bool = True):
    """Transcribes audio streamed from the microphone using Google Cloud Speech-to-Text.

    Args:
        language_code: The language code for recognition (e.g., "en-US").
        enable_punctuation: Whether to enable automatic punctuation.

    Yields:
        google.cloud.speech_v1p1beta1.StreamingRecognizeResponse: 
            Responses containing interim and final transcripts.
    """
    client = get_speech_client()
    config, streaming_config = create_streaming_config(language_code, enable_punctuation)

    requests = (
        types.StreamingRecognizeRequest(audio_content=chunk)
        for chunk in stream_microphone_audio()
    )

    # The first request must contain the streaming config
    yield from client.streaming_recognize(
        streaming_config=streaming_config, config=config, requests=requests
    )
