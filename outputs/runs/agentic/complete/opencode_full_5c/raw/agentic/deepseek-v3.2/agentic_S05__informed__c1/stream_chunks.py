import asyncio
from deepgram import Deepgram
import os


async def stream_audio_chunks(audio_source):
    dg_client = Deepgram(os.getenv("DEEPGRAM_API_KEY"))

    async with dg_client.transcription.live(
        {
            "model": "nova-2",
            "interim_results": True,
            "smart_format": True,
            "encoding": "linear16",
            "sample_rate": 16000,
            "channels": 1,
        }
    ) as connection:

        async def send_chunks():
            async for chunk in audio_source:
                await connection.send(chunk)

        async def receive_transcripts():
            async for message in connection:
                if "channel" in message:
                    for alternative in message["channel"]["alternatives"]:
                        if "transcript" in alternative:
                            transcript = alternative["transcript"]
                            if transcript:
                                is_final = message.get("is_final", False)
                                yield transcript, is_final

        send_task = asyncio.create_task(send_chunks())

        try:
            async for transcript, is_final in receive_transcripts():
                yield transcript, is_final
        finally:
            send_task.cancel()
            try:
                await send_task
            except asyncio.CancelledError:
                pass


class AsyncAudioSource:
    def __init__(self, chunks):
        self.chunks = chunks

    def __aiter__(self):
        self.index = 0
        return self

    async def __anext__(self):
        if self.index >= len(self.chunks):
            raise StopAsyncIteration
        chunk = self.chunks[self.index]
        self.index += 1
        await asyncio.sleep(0.01)
        return chunk


async def example_usage():
    test_chunks = [b"\x00" * 1024 for _ in range(10)]
    source = AsyncAudioSource(test_chunks)

    async for transcript, is_final in stream_audio_chunks(source):
        print(f"{'INTERIM' if not is_final else 'FINAL'}: {transcript}")


if __name__ == "__main__":
    asyncio.run(example_usage())
