import asyncio
import json
import os
import queue
import threading
from typing import AsyncGenerator, Optional

import sounddevice as sd
from deepgram import DeepgramClient, LiveOptions, LiveTranscriptionEvents


class MicrophoneTranscriptStream:
    def __init__(self, model: str = "nova-2", sample_rate: int = 16000, channels: int = 1) -> None:
        self.model = model
        self.sample_rate = sample_rate
        self.channels = channels
        self._audio_queue: "queue.Queue[bytes]" = queue.Queue()
        self._stop_event = threading.Event()

    def _audio_callback(self, indata, frames, time, status) -> None:
        if status:
            pass
        self._audio_queue.put(bytes(indata))

    async def stream(self) -> AsyncGenerator[str, None]:
        api_key = os.environ.get("DEEPGRAM_API_KEY")
        if not api_key:
            raise RuntimeError("DEEPGRAM_API_KEY is required")

        client = DeepgramClient(api_key)
        connection = client.listen.asynclive.v("1")

        loop = asyncio.get_running_loop()
        transcript_queue: "asyncio.Queue[Optional[str]]" = asyncio.Queue()

        def on_message(_, result, **kwargs) -> None:
            try:
                payload = json.loads(result.to_json()) if hasattr(result, "to_json") else result
                channel = payload.get("channel", {})
                alternatives = channel.get("alternatives", [])
                transcript = alternatives[0].get("transcript", "") if alternatives else ""
                if transcript:
                    loop.call_soon_threadsafe(transcript_queue.put_nowait, transcript)
            except Exception:
                return

        def on_close(_, **kwargs) -> None:
            loop.call_soon_threadsafe(transcript_queue.put_nowait, None)

        connection.on(LiveTranscriptionEvents.Transcript, on_message)
        connection.on(LiveTranscriptionEvents.Close, on_close)

        options = LiveOptions(
            model=self.model,
            language="en-US",
            smart_format=True,
            interim_results=True,
            punctuate=True,
            encoding="linear16",
            channels=self.channels,
            sample_rate=self.sample_rate,
        )

        await connection.start(options)

        def mic_worker() -> None:
            with sd.RawInputStream(
                samplerate=self.sample_rate,
                blocksize=8000,
                channels=self.channels,
                dtype="int16",
                callback=self._audio_callback,
            ):
                while not self._stop_event.is_set():
                    try:
                        data = self._audio_queue.get(timeout=0.1)
                    except queue.Empty:
                        continue
                    asyncio.run_coroutine_threadsafe(connection.send(data), loop)

        worker = threading.Thread(target=mic_worker, daemon=True)
        worker.start()

        try:
            while True:
                item = await transcript_queue.get()
                if item is None:
                    break
                yield item
        finally:
            self._stop_event.set()
            try:
                await connection.finish()
            except Exception:
                pass


async def stream_microphone() -> AsyncGenerator[str, None]:
    async for transcript in MicrophoneTranscriptStream().stream():
        yield transcript
