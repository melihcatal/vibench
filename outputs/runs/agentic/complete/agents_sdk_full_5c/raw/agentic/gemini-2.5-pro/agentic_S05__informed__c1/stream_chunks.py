import asyncio
from deepgram import LiveTranscriptionEvents
from speech_client import get_deepgram_client

async def get_audio_chunks():
    """An async generator that yields simulated audio chunks."""
    chunk_size = 4096
    for _ in range(10):
        await asyncio.sleep(0.2)
        yield b'\x00' * chunk_size

async def stream_from_chunks():
    """Streams audio from an async generator of chunks and prints the transcript."""
    deepgram_client = get_deepgram_client()
    
    try:
        dg_connection = deepgram_client.listen.asynclive.v("1")

        async def on_message(self, result, **kwargs):
            sentence = result.channel.alternatives[0].transcript
            if sentence:
                print(f"Received: {sentence}")

        dg_connection.on(LiveTranscriptionEvents.Transcript, on_message)

        options = { "model": "nova-2", "language": "en-US" }
        await dg_connection.start(options)

        async for chunk in get_audio_chunks():
            await dg_connection.send(chunk)

        await dg_connection.finish()

    except Exception as e:
        print(f"An error occurred: {e}")
