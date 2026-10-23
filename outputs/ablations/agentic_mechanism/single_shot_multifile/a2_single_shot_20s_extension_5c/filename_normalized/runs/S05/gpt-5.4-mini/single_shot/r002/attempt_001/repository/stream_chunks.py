import asyncio
from typing import AsyncIterator, Iterable, Optional

from openai import AsyncOpenAI

from speech_client import build_openai_client, get_openai_model
from speech_models import StreamingTranscript, normalize_transcript


class AsyncChunkSource:
    def __init__(self, chunks: Iterable[bytes]) -> None:
        self._chunks = list(chunks)

    async def __aiter__(self) -> AsyncIterator[bytes]:
        for chunk in self._chunks:
            await asyncio.sleep(0)
            yield chunk


async def stream_chunks(source: AsyncIterator[bytes]) -> AsyncIterator[StreamingTranscript]:
    client: AsyncOpenAI = build_openai_client()
    model = get_openai_model()
    buffer = bytearray()
    async for chunk in source:
        buffer.extend(chunk)
        if len(buffer) < 24000:
            continue
        result = await client.audio.transcriptions.create(
            model=model,
            file=("chunk.wav", bytes(buffer), "audio/wav"),
            response_format="verbose_json",
        )
        text = normalize_transcript(getattr(result, "text", ""))
        if text:
            yield StreamingTranscript(text=text, is_final=False, language=getattr(result, "language", None))
        buffer.clear()


async def main() -> None:
    async def gen() -> AsyncIterator[bytes]:
        yield b"\x00\x00" * 16000
        yield b"\x01\x01" * 16000

    async for item in stream_chunks(gen()):
        print(item.text)


if __name__ == "__main__":
    asyncio.run(main())
