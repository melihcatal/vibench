import asyncio
from deepgram import Deepgram
from speech_client import get_deepgram_client
from speech_models import TranscriptEvent

deepgram = get_deepgram_client()

async def stream_chunks(audio_chunks):
    dg_connection = await deepgram.transcription.live({
        "punctuate": True,
        "interim_results": True,
        "language": "en-US",
        "model": "nova-2"
    })

    async def send_audio():
        async for chunk in audio_chunks:
            await dg_connection.send(chunk)
            await asyncio.sleep(0.1)
        await dg_connection.finish()

    async def receive_transcripts():
        async for event in dg_connection:
            transcript_event = TranscriptEvent.from_deepgram(event)
            if transcript_event:
                yield transcript_event

    send_task = asyncio.create_task(send_audio())
    try:
        async for transcript in receive_transcripts():
            yield transcript
    finally:
        send_task.cancel()