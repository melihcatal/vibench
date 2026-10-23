import os
import asyncio
import pyaudio
from google.cloud import speech_v1p1beta1 as speech
from google.cloud.speech_v1p1beta1 import types
from speech_client import get_speech_client
from speech_models import StreamingRecognitionConfig, PartialResult, FinalResult


class MicrophoneStream:
    """Opens a recording stream from the microphone."""

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

    async def generator(self):
        while not self._closed:
            chunk = await self._buffer.get()
            if chunk is None:
                return
            yield chunk

    def close(self):
        self._audio_stream.stop_stream()
        self._audio_stream.close()
        self._closed = True
        self._buffer.put_nowait(None)
        self._audio_interface.terminate()


async def stream_microphone():
    """Streams microphone audio and yields interim transcripts."""
    client = get_speech_client()
    config = StreamingRecognitionConfig(
        language_code="en-US",
        enable_automatic_punctuation=True,
        interim_results=True,
    )

    mic_stream = MicrophoneStream(rate=16000, chunk=8192)
    audio_generator = mic_stream.generator()

    requests = (
        types.StreamingRecognizeRequest(audio_content=chunk)
        for chunk in audio_generator
    )

    streaming_config = types.StreamingRecognitionConfig(
        config=config.to_grpc(),
        interim_results=True,
    )

    responses = client.streaming_recognize(streaming_config, requests)

    async for response in responses:
        for result in response.results:
            if result.is_final:
                yield FinalResult.from_grpc(result)
            else:
                yield PartialResult.from_grpc(result)

    mic_stream.close()
