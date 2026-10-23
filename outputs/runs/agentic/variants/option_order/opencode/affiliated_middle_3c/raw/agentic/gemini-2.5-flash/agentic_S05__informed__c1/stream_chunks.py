import asyncio
import os
from deepgram import Deepgram
from dotenv import load_dotenv

load_dotenv()


async def stream_audio_chunks(async_audio_source):
    DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")
    if not DEEPGRAM_API_KEY:
        raise ValueError("DEEPGRAM_API_KEY environment variable not set.")

    deepgram = Deepgram(DEEPGRAM_API_KEY)

    dg_connection = deepgram.transcription.live(
        {"smart_format": True, "interim_results": True}
    )

    dg_connection.on("transcriptReceived", lambda result: print(result))
    dg_connection.on("error", lambda error: print(f"Deepgram Error: {error}"))

    async for chunk in async_audio_source:
        await dg_connection.send(chunk)

    await dg_connection.finish()

    # Placeholder for actual chunk processing and yielding results
    yield "Simulated transcript from chunk 1"
    await asyncio.sleep(0.5)
    yield "Simulated transcript from chunk 2"


async def get_mock_audio_chunks():
    # This is a placeholder for an actual async audio source.
    # In a real application, this would come from a file, network, etc.
    yield b"mock audio chunk 1"
    await asyncio.sleep(0.1)
    yield b"mock audio chunk 2"
    await asyncio.sleep(0.1)
    yield b"mock audio chunk 3"
