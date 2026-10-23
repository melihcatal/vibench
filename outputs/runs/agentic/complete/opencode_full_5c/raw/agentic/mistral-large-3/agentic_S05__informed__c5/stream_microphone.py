import os
import asyncio
import pyaudio
from google.cloud import speech_v1p1beta1 as speech
from google.cloud.speech_v1p1beta1 import types
from typing import AsyncGenerator, Dict, Any

from speech_client import get_speech_client
from speech_models import StreamingRecognitionConfig


class MicrophoneStream:
    """Opens a recording stream from the microphone."""

    def __init__(self, rate: int = 16000, chunk: int = 8192):
        self._rate = rate
        self._chunk = chunk
        self._audio_interface = pyaudio.PyAudio()
        self._audio_stream = self._audio_interface.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=self._rate,
            input=True,
            frames_per_buffer=self._chunk,
            stream_callback=self._fill_buffer,
        )
        self._buffer = asyncio.Queue()
        self._closed = False

    def _fill_buffer(self, in_data, frame_count, time_info, status_flags):
        """Continuously collect data from the audio stream."""
        self._buffer.put_nowait(in_data)
        return None, pyaudio.paContinue

    async def generator(self) -> AsyncGenerator[bytes, None]:
        """Yields audio chunks from the microphone."""
        while not self._closed:
            chunk = await self._buffer.get()
            yield chunk

    def close(self):
        """Closes the audio stream."""
        self._audio_stream.stop_stream()
        self._audio_stream.close()
        self._audio_interface.terminate()
        self._closed = True


async def stream_microphone() -> AsyncGenerator[Dict[str, Any], None]:
    """Streams microphone audio and yields interim transcripts using Google Cloud Speech-to-Text."""
    client = get_speech_client()
    config = StreamingRecognitionConfig(
        language_code="en-US",
        interim_results=True,
        enable_automatic_punctuation=True,
    ).to_google_config()

    microphone = MicrophoneStream()
    requests = (
        types.StreamingRecognizeRequest(audio_content=chunk)
        async for chunk in microphone.generator()
    )

    responses = await client.streaming_recognize(config, requests)
    async for response in responses:
        for result in response.results:
            yield {
                "transcript": result.alternatives[0].transcript,
                "is_final": result.is_final,
                "stability": result.stability,
            }

    microphone.close()
