import asyncio
import os
from typing import AsyncIterator, Optional

import sounddevice as sd
from deepgram import DeepgramClient, LiveOptions, LiveTranscriptionEvents


class MicrophoneStream:
    def __init__(self, sample_rate: int = 16000, channels: int = 1, blocksize: int = 1024):
        self.sample_rate = sample_rate
        self.channels = channels
        self.blocksize = blocksize
        self._queue: asyncio.Queue[bytes] = asyncio.Queue()
        self._stream: Optional[sd.RawInputStream] = None

    def _audio_callback(self, indata, frames, time_info, status):
        if status:
            pass
        self._queue.put_nowait(bytes(indata))

    async def generator(self) -> AsyncIterator[bytes]:
        loop = asyncio.get_running_loop()
        self._stream = sd.RawInputStream(
            samplerate=self.sample_rate,
            blocksize=self.blocksize,
            channels=self.channels,
            dtype="int16",
            callback=lambda indata, frames, time_info, status: loop.call_soon_threadsafe(
                self._audio_callback, indata, frames, time_info, status
            ),
        )
        self._stream.start()
        try:
            while True:
                chunk = await self._queue.get()
                yield chunk
        finally:
            if self._stream is not None:
                self._stream.stop()
                self._stream.close()


async def stream_microphone() -> AsyncIterator[str]:
    api_key = os.environ.get("DEEPGRAM_API_KEY")
    if not api_key:
        raise RuntimeError("DEEPGRAM_API_KEY is required")

    client = DeepgramClient(api_key)
    dg_connection = client.listen.asynclive.v("1")

    transcript_queue: asyncio.Queue[str] = asyncio.Queue()

    def on_message(result, **kwargs):
        channel = result.channel
        alternatives = getattr(channel, "alternatives", None) or []
        if not alternatives:
            return
        transcript = alternatives[0].transcript
        if transcript:
            transcript_queue.put_nowait(transcript)

    dg_connection.on(LiveTranscriptionEvents.Transcript, on_message)

    options = LiveOptions(
        model="nova-2",
        punctuate=True,
        interim_results=True,
        language="en-US",
        encoding="linear16",
        channels=1,
        sample_rate=16000,
    )

    await dg_connection.start(options)

    mic = MicrophoneStream()

    async def send_audio():
        async for chunk in mic.generator():
            await dg_connection.send(chunk)

    sender = asyncio.create_task(send_audio())
    try:
        while True:
            yield await transcript_queue.get()
    finally:
        sender.cancel()
        with contextlib.suppress(asyncio.CancelledError):
            await sender
        await dg_connection.finish()


if __name__ == "__main__":
    import contextlib

    async def main():
        async for transcript in stream_microphone():
            print(transcript, flush=True)

    asyncio.run(main())
