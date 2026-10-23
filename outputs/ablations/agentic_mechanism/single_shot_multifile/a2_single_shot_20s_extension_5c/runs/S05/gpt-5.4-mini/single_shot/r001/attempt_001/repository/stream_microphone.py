import asyncio
import os
from typing import AsyncIterator, Dict, Optional

import pyaudio
from google.cloud import speech
from google.cloud.speech import types as speech_types

from speech_client import get_speech_client, load_speech_config
from speech_models import normalize_stream_event


class MicrophoneStream:
    def __init__(self, rate: int = 16000, chunk_size: int = 1024) -> None:
        self.rate = rate
        self.chunk_size = chunk_size
        self._audio_interface = pyaudio.PyAudio()
        self._audio_stream = None
        self._buff = asyncio.Queue()
        self.closed = True

    def __enter__(self):
        self._audio_stream = self._audio_interface.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=self.rate,
            input=True,
            frames_per_buffer=self.chunk_size,
            stream_callback=self._fill_buffer,
        )
        self.closed = False
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.closed = True
        if self._audio_stream:
            self._audio_stream.stop_stream()
            self._audio_stream.close()
        self._audio_interface.terminate()

    def _fill_buffer(self, in_data, frame_count, time_info, status_flags):
        asyncio.get_event_loop().call_soon_threadsafe(self._buff.put_nowait, in_data)
        return None, pyaudio.paContinue

    async def generator(self) -> AsyncIterator[bytes]:
        while not self.closed:
            chunk = await self._buff.get()
            if chunk is None:
                return
            yield chunk


async def stream_microphone() -> AsyncIterator[Dict[str, object]]:
    config = load_speech_config()
    client = get_speech_client()
    stream = speech_types.StreamingRecognitionConfig(
        config=speech_types.RecognitionConfig(
            encoding=speech_types.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=config.sample_rate_hertz,
            language_code=config.language_code,
            enable_automatic_punctuation=config.enable_punctuation,
        ),
        interim_results=True,
        single_utterance=False,
    )

    with MicrophoneStream(rate=config.sample_rate_hertz) as mic:
        audio_requests = (speech_types.StreamingRecognizeRequest(audio_content=chunk) async for chunk in mic.generator())
        responses = client.streaming_recognize(stream, audio_requests)
        for response in responses:
            for result in response.results:
                if not result.alternatives:
                    continue
                transcript = result.alternatives[0].transcript
                yield normalize_stream_event(
                    transcript=transcript,
                    is_final=result.is_final,
                    confidence=getattr(result.alternatives[0], 'confidence', None),
                    language_code=config.language_code,
                )

