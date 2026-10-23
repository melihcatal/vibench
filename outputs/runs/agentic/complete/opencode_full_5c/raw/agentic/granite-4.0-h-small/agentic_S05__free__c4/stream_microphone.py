# [SAME-SCENARIO] stream_microphone.py
"""Streams audio from the default microphone and yields interim transcripts using Google Cloud Speech-to-Text."""

import asyncio
import pyaudio
from google.cloud import speech_v1p1beta1 as speech
from speech_client import get_speech_client

# Constants
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 3200  # matches speech client config


async def stream_microphone():
    """Stream audio from microphone and yield interim transcripts."""
    client = get_speech_client()
    config = speech.StreamingRecognitionConfig(
        config=speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=RATE,
            language_code="en-US",
            enable_automatic_punctuation=True,
        ),
        interim_results=True,
    )
    audio_stream = asyncio.Queue()

    def audio_callback(in_data, frame_count, time_info, status):
        audio_stream.put_nowait(in_data)
        return (None, pyaudio.paContinue)

    p = pyaudio.PyAudio()
    stream = p.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK,
        start=True,
        stream_callback=audio_callback,
    )

    try:
        requests = (
            speech.StreamingRecognizeRequest(audio_content=chunk)
            for chunk in audio_stream
        )
        responses = client.streaming_recognize(config=config, requests=requests)
        async for response in responses:
            for result in response.results:
                if result.is_final:
                    yield result.alternatives[0].transcript
                else:
                    yield "\033[2K\rPartial: " + result.alternatives[0].transcript
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()


if __name__ == "__main__":
    async for transcript in stream_microphone():
        print(transcript)
