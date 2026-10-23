import asyncio
import os
from typing import AsyncIterator, Optional

import sounddevice as sd
from openai import AsyncOpenAI

from speech_client import build_openai_client, get_openai_model
from speech_models import StreamingTranscript, normalize_transcript


class MicrophoneStreamer:
    def __init__(self, sample_rate: int = 16000, blocksize: int = 1024) -> None:
        self.sample_rate = sample_rate
        self.blocksize = blocksize

    async def audio_chunks(self) -> AsyncIterator[bytes]:
        loop = asyncio.get_running_loop()
        queue: asyncio.Queue[Optional[bytes]] = asyncio.Queue()

        def callback(indata, frames, time, status):
            if status:
                pass
            loop.call_soon_threadsafe(queue.put_nowait, bytes(indata))

        with sd.RawInputStream(
            samplerate=self.sample_rate,
            blocksize=self.blocksize,
            dtype="int16",
            channels=1,
            callback=callback,
        ):
            while True:
                chunk = await queue.get()
                if chunk is None:
                    break
                yield chunk


async def stream_microphone() -> AsyncIterator[StreamingTranscript]:
    client: AsyncOpenAI = build_openai_client()
    model = get_openai_model()
    streamer = MicrophoneStreamer()
    buffer = bytearray()
    max_buffer_bytes = int(os.getenv("OPENAI_STT_MAX_BUFFER_BYTES", "32000"))

    async for chunk in streamer.audio_chunks():
        buffer.extend(chunk)
        if len(buffer) < max_buffer_bytes:
            continue
        transcription = await client.audio.transcriptions.create(
            model=model,
            file=("mic.wav", bytes(buffer), "audio/wav"),
            response_format="verbose_json",
            temperature=0,
        )
        text = normalize_transcript(getattr(transcription, "text", ""))
        if text:
            yield StreamingTranscript(text=text, is_final=False, language=getattr(transcription, "language", None))
        buffer.clear()


async def main() -> None:
    async for item in stream_microphone():
        print(item.text)


if __name__ == "__main__":
    asyncio.run(main())
