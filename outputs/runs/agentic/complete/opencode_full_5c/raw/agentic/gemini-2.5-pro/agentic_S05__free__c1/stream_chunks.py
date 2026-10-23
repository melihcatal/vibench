import asyncio
import random
from speech_client import get_speech_client
from deepgram.clients.live.v1 import LiveClient, LiveTranscriptionEvents


async def get_audio_chunk():
    """A dummy async generator for audio chunks."""
    for _ in range(5):
        await asyncio.sleep(0.5)
        # Yielding dummy bytes
        yield bytes([random.randint(0, 255) for _ in range(1024)])


async def stream_chunks():
    try:
        deepgram_client = get_speech_client()
        dg_connection: LiveClient = deepgram_client.listen.asynclive.v("1")

        async def on_message(self, result, **kwargs):
            sentence = result.channel.alternatives[0].transcript
            if len(sentence) > 0:
                print(f"Transcript: {sentence}")

        dg_connection.on(LiveTranscriptionEvents.Transcript, on_message)

        # Start the connection
        await dg_connection.start()

        # Stream chunks from the async source
        async for chunk in get_audio_chunk():
            await dg_connection.send(chunk)

        # Finish the connection
        await dg_connection.finish()

    except Exception as e:
        print(f"Error during streaming: {e}")


if __name__ == "__main__":
    asyncio.run(stream_chunks())
