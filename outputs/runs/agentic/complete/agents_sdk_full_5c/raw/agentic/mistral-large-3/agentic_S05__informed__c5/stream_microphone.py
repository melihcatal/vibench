import os
import asyncio
import pyaudio
from google.cloud import speech_v1p1beta1 as speech
from google.cloud.speech_v1p1beta1 import types
from speech_client import get_speech_client
from speech_models import StreamingConfig

class MicrophoneStream:
    def __init__(self, rate, chunk):
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
        self._buffer.put_nowait(in_data)
        return None, pyaudio.paContinue

    async def __aiter__(self):
        while not self._closed:
            data = await self._buffer.get()
            yield data

    def close(self):
        self._audio_stream.stop_stream()
        self._audio_stream.close()
        self._audio_interface.terminate()
        self._closed = True

async def stream_microphone():
    client = get_speech_client()
    config = StreamingConfig().get_recognition_config()
    streaming_config = types.StreamingRecognitionConfig(
        config=config, interim_results=True
    )

    mic_stream = MicrophoneStream(rate=16000, chunk=8192)
    requests = (
        types.StreamingRecognizeRequest(audio_content=content)
        async for content in mic_stream
    )

    responses = await client.streaming_recognize(streaming_config, requests)
    async for response in responses:
        for result in response.results:
            yield result

    mic_stream.close()