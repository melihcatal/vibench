import asyncio
from typing import AsyncGenerator

from deepgram import LiveOptions

from speech_client import get_speech_client

async def get_audio_chunks() -> AsyncGenerator[bytes, None]:
    """
    An asynchronous generator that yields dummy audio chunks.
    In a real application, this could be reading from a file, a network stream, etc.
    """
    chunk_size = 1024
    for _ in range(100):  # Simulate 100 chunks of audio
        yield b'\x00' * chunk_size
        await asyncio.sleep(0.05)

async def stream_audio_chunks():
    """
    Streams audio chunks from an async source to Deepgram for transcription.
    """
    deepgram_client = get_speech_client()
    
    try:
        dg_connection = deepgram_client.listen.asynclive.v("1")

        async def on_message(self, result, **kwargs):
            sentence = result.channel.alternatives[0].transcript
            if len(sentence) > 0:
                print(f"Transcript: {sentence}")

        dg_connection.on("transcript", on_message)

        options = LiveOptions(
            model="nova-2",
            language="en-US",
            encoding="linear16",
            channels=1,
            sample_rate=16000,
        )
        await dg_connection.start(options)

        async for chunk in get_audio_chunks():
            await dg_connection.send(chunk)

        await dg_connection.finish()
        print("Finished streaming chunks.")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(stream_audio_chunks())
