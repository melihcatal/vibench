import asyncio
import queue
import threading
from typing import AsyncGenerator, Optional

import pyaudio

from speech_client import (
    create_deepgram_client,
    build_live_options,
    register_default_handlers,
)
from speech_models import (
    TranscriptResult,
    TranscriptType,
    parse_deepgram_result,
    AudioChunk,
)
from deepgram.clients.live.v1 import LiveTranscriptionEvents

CHUNK_SIZE = 4096
SAMPLE_RATE = 16000
CHANNELS = 1
FORMAT = pyaudio.paInt16


class MicrophoneStream:
    def __init__(
        self,
        sample_rate: int = SAMPLE_RATE,
        channels: int = CHANNELS,
        chunk_size: int = CHUNK_SIZE,
        device_index: Optional[int] = None,
    ):
        self.sample_rate = sample_rate
        self.channels = channels
        self.chunk_size = chunk_size
        self.device_index = device_index
        self._audio = pyaudio.PyAudio()
        self._stream = None
        self._running = False
        self._queue: queue.Queue = queue.Queue()
        self._thread: Optional[threading.Thread] = None

    def start(self):
        self._stream = self._audio.open(
            format=FORMAT,
            channels=self.channels,
            rate=self.sample_rate,
            input=True,
            frames_per_buffer=self.chunk_size,
            input_device_index=self.device_index,
            stream_callback=self._audio_callback,
        )
        self._running = True
        self._thread = threading.Thread(target=self._stream.start, daemon=True)
        self._thread.start()

    def _audio_callback(self, in_data, frame_count, time_info, status):
        if self._running:
            self._queue.put(in_data)
        return (None, pyaudio.paContinue)

    def read_chunk(self, timeout: float = 1.0) -> Optional[bytes]:
        try:
            return self._queue.get(timeout=timeout)
        except queue.Empty:
            return None

    def stop(self):
        self._running = False
        if self._stream:
            self._stream.stop_stream()
            self._stream.close()
        self._audio.terminate()

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, *args):
        self.stop()


async def stream_microphone_audio(
    sample_rate: int = SAMPLE_RATE,
    channels: int = CHANNELS,
    chunk_size: int = CHUNK_SIZE,
    device_index: Optional[int] = None,
    timeout: float = 1.0,
) -> AsyncGenerator[AudioChunk, None]:
    mic = MicrophoneStream(
        sample_rate=sample_rate,
        channels=channels,
        chunk_size=chunk_size,
        device_index=device_index,
    )
    try:
        mic.start()
        while True:
            data = mic.read_chunk(timeout=timeout)
            if data is None:
                continue
            yield AudioChunk(
                data=data,
                sample_rate=sample_rate,
                channels=channels,
            )
    finally:
        mic.stop()


async def stream_microphone_with_transcripts(
    model: str = "nova-2",
    language: str = "en-US",
    sample_rate: int = SAMPLE_RATE,
    channels: int = CHANNELS,
    chunk_size: int = CHUNK_SIZE,
    punctuate: bool = True,
    smart_format: bool = True,
    interim_results: bool = True,
    device_index: Optional[int] = None,
):
    client = create_deepgram_client()
    options = build_live_options(
        model=model,
        language=language,
        sample_rate=sample_rate,
        channels=channels,
        punctuate=punctuate,
        smart_format=smart_format,
        interim_results=interim_results,
    )

    result_queue: asyncio.Queue = asyncio.Queue()

    def on_transcript(self_conn, result, **kwargs):
        parsed = parse_deepgram_result(result)
        asyncio.get_event_loop().call_soon_threadsafe(result_queue.put_nowait, parsed)

    async with client.listen.asyncwebsocket.v("1") as ws:
        register_default_handlers(ws, on_interim=on_transcript)
        await ws.start(options)

        async for audio_chunk in stream_microphone_audio(
            sample_rate=sample_rate,
            channels=channels,
            chunk_size=chunk_size,
            device_index=device_index,
        ):
            await ws.send(audio_chunk.data)

            while not result_queue.empty():
                transcript_result = await result_queue.get()
                yield transcript_result

        await ws.finalize()
