import asyncio
from deepgram import LiveTranscriptionEvents
from speech_client import get_deepgram_client
from speech_models import StreamingTranscript

async def get_simulated_audio():
    """Simulates a short stream of audio chunks."""
    for _ in range(15):
        yield b'\x00' * 2048
        await asyncio.sleep(0.1)

async def handle_partial_and_final_results():
    """
    Connects to Deepgram and demonstrates handling of partial
    and final transcription results.
    """
    deepgram_client = get_deepgram_client()
    dg_connection = deepgram_client.listen.asynclive.v("1")

    async def on_transcript(self, result: StreamingTranscript, **kwargs):
        transcript = result.channel.alternatives[0].transcript
        if not transcript:
            return

        if result.is_final:
            print(f"Final Transcript: {transcript}")
        else:
            print(f"Partial Transcript: {transcript}")

    dg_connection.on(LiveTranscriptionEvents.Transcript, on_transcript)

    options = {
        "model": "nova-2",
        "language": "en-US",
        "interim_results": True, # Crucial for getting partial results
    }
    await dg_connection.start(options)

    async for chunk in get_simulated_audio():
        await dg_connection.send(chunk)

    await dg_connection.finish()
