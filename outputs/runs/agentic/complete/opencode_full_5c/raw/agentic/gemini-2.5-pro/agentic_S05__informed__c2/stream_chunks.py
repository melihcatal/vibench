import asyncio
import os
from dotenv import load_dotenv

from deepgram import (
    DeepgramClient,
    LiveTranscriptionEvents,
    LiveOptions,
)

load_dotenv()


async def stream_chunks(async_chunk_source):
    try:
        deepgram = DeepgramClient(os.getenv("DEEPGRAM_API_KEY"))

        dg_connection = deepgram.listen.asynclive.v("1")

        async def on_message(self, result, **kwargs):
            sentence = result.channel.alternatives[0].transcript
            if len(sentence) > 0:
                print(f"transcript: {sentence}")

        dg_connection.on(LiveTranscriptionEvents.Transcript, on_message)

        options = LiveOptions(
            model="nova-2",
            language="en-US",
            encoding="linear16",
            channels=1,
            sample_rate=16000,
        )
        await dg_connection.start(options)

        async for chunk in async_chunk_source:
            dg_connection.send(chunk)

        await dg_connection.finish()

    except Exception as e:
        print(f"Error during streaming: {e}")


async def get_audio_chunks():
    # This is a placeholder for a real async audio source
    # For example, reading from a file, a network stream, etc.
    # Here we simulate it with empty chunks.
    for i in range(10):
        await asyncio.sleep(0.5)
        yield b"\x00" * 3200  # Simulate 100ms of 16kHz 16-bit mono audio


if __name__ == "__main__":
    asyncio.run(stream_chunks(get_audio_chunks()))
