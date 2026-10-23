import asyncio
from typing import AsyncGenerator
from deepgram import LiveTranscriptionEvents
from speech_client import get_deepgram_client, get_live_options


async def stream_audio_chunks(audio_source: AsyncGenerator[bytes, None]):
    """
    Streams audio chunks from an async generator source and prints transcripts.
    """
    client = get_deepgram_client()
    options = get_live_options()
    dg_connection = client.listen.asynclive.v("1")
    transcripts = []

    async def on_message(self, result, **kwargs):
        sentence = result.channel.alternatives[0].transcript
        if sentence:
            transcripts.append(sentence)
            print(f"Transcript from chunk: {sentence}")

    dg_connection.on(LiveTranscriptionEvents.Transcript, on_message)
    await dg_connection.start(options)

    async for chunk in audio_source:
        await dg_connection.send(chunk)
        await asyncio.sleep(0.01)

    await dg_connection.finish()
    return transcripts
