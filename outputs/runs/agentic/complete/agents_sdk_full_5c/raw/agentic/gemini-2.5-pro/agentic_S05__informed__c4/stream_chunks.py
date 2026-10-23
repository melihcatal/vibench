import asyncio
from typing import AsyncGenerator
from speech_client import get_speech_client
from deepgram import LiveOptions, LiveTranscriptionEvents

async def audio_chunk_generator() -> AsyncGenerator[bytes, None]:
    """A dummy async generator that yields empty audio chunks."""
    for i in range(5):
        yield b'\x00' * 3200  # Simulate 100ms of 16kHz 16-bit mono audio
        await asyncio.sleep(0.1)

async def stream_audio_chunks(chunks: AsyncGenerator[bytes, None]):
    """Streams audio chunks from an async generator to Deepgram."""
    deepgram_client = get_speech_client()
    
    try:
        dg_connection = deepgram_client.listen.asynclive.v("1")

        async def on_message(self, result, **kwargs):
            sentence = result.channel.alternatives[0].transcript
            if len(sentence):
                print(f"Transcript: {sentence}")

        dg_connection.on(LiveTranscriptionEvents.Transcript, on_message)

        options = LiveOptions(model="nova-2", language="en-US")
        await dg_connection.start(options)

        async for chunk in chunks:
            await dg_connection.send(chunk)

        await dg_connection.finish()
        print("Finished processing chunks.")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # This example demonstrates streaming from an async source.
    # asyncio.run(stream_audio_chunks(audio_chunk_generator()))
    print("stream_chunks.py contains a runnable example. Please uncomment the last line to run.")
