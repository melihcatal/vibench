import asyncio
import os
from deepgram import Deepgram
from dotenv import load_dotenv

load_dotenv()


async def stream_microphone_audio():
    DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")
    if not DEEPGRAM_API_KEY:
        raise ValueError("DEEPGRAM_API_KEY environment variable not set.")

    deepgram = Deepgram(DEEPGRAM_API_KEY)

    # This is a placeholder for actual microphone streaming logic.
    # In a real application, you would capture audio from the microphone
    # and send it to Deepgram.
    # For demonstration, we simulate yielding interim transcripts.
    print("Simulating microphone stream... (replace with actual audio capture)")
    source = {"buffer": b"Simulated audio data", "mimetype": "audio/wav"}

    # Placeholder for Deepgram connection
    dg_connection = deepgram.transcription.live(
        {"smart_format": True, "interim_results": True}
    )

    dg_connection.on("transcriptReceived", lambda result: print(result))
    dg_connection.on("error", lambda error: print(f"Deepgram Error: {error}"))

    await dg_connection.send(source["buffer"])
    await dg_connection.finish()

    yield "Simulated interim transcript 1"
    await asyncio.sleep(1)
    yield "Simulated interim transcript 2"
