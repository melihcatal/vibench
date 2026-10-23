import os
import asyncio
from deepgram import DeepgramClient, LiveTranscriptionEvents, LiveOptions
from speech_client import get_deepgram_client
from speech_models import TranscriptEvent

DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")

async def stream_chunks(audio_chunk_stream):
    deepgram = get_deepgram_client()
    dg_connection = deepgram.listen.asynclive.v("1")

    async def on_message(self, result, **kwargs):
        transcript = result.channel.alternatives[0].transcript
        if transcript:
            event = TranscriptEvent(
                text=transcript,
                is_final=result.is_final,
                confidence=result.channel.alternatives[0].confidence
            )
            yield event

    dg_connection.on(LiveTranscriptionEvents.TranscriptReceived, on_message)

    options = LiveOptions(
        model="nova-2",
        language="en-US",
        smart_format=True,
        interim_results=True,
        punctuate=True
    )

    await dg_connection.start(options)

    try:
        async for chunk in audio_chunk_stream:
            await dg_connection.send(chunk)
            await asyncio.sleep(0.05)
    except asyncio.CancelledError:
        await dg_connection.finish()

async def chunk_transcript_stream(audio_chunk_stream):
    async for event in stream_chunks(audio_chunk_stream):
        yield event