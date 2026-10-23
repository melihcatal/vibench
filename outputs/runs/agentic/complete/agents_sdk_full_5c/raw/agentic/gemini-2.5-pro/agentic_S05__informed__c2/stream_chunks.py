from dotenv import load_dotenv
from deepgram import DeepgramClient, LiveTranscriptionEvents
from deepgram.options import LiveOptions
import logging
import asyncio
import aiofiles

from speech_client import get_speech_client
from speech_models import TranscriptChunk

load_dotenv()

# Example async generator to simulate streaming audio chunks from a source
async def get_audio_chunks():
    """An async generator that yields audio chunks from a file."""
    # This is a placeholder for a real audio stream (e.g., from a network socket)
    chunk_size = 4096
    try:
        async with aiofiles.open("sample_audio.wav", "rb") as f:
            while True:
                data = await f.read(chunk_size)
                if not data:
                    break
                yield data
    except FileNotFoundError:
        logging.warning("sample_audio.wav not found. Yielding empty chunks.")
        # Yield a few empty chunks to let the connection establish and close
        for _ in range(5):
            yield b""
            await asyncio.sleep(0.1)


async def stream_audio_chunks():
    """Streams audio chunks from an async source and yields transcript chunks."""
    try:
        deepgram = get_speech_client()
        dg_connection = deepgram.listen.asynclive.v("1")

        async def on_message(self, result, **kwargs):
            sentence = result.channel.alternatives[0].transcript
            if len(sentence) > 0:
                is_final = result.is_final
                chunk = TranscriptChunk(text=sentence, is_final=is_final)
                print(f"Received: {chunk}")

        dg_connection.on(LiveTranscriptionEvents.Transcript, on_message)
        
        options = LiveOptions(model="nova-2", language="en-US")
        await dg_connection.start(options)

        async for chunk in get_audio_chunks():
            await dg_connection.send(chunk)

        await dg_connection.finish()
        logging.info("Finished streaming chunks.")

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    # Create a dummy audio file for demonstration if it doesn't exist
    try:
        with open("sample_audio.wav", "wb") as f:
             # A simple silent WAV header and some empty data
            f.write(b'RIFF$\x00\x00\x00WAVEfmt \x10\x00\x00\x00\x01\x00\x01\x00\x80>\x00\x00\x00\xfa\x00\x00\x02\x00\x10\x00data\x00\x00\x00\x00')
    except IOError:
        pass
    asyncio.run(stream_audio_chunks())
