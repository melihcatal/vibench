import asyncio
from typing import AsyncGenerator, AsyncIterable, Dict, Any
from deepgram import LiveTranscriptionEvents
from speech_client import get_speech_client
from speech_models import get_live_options

async def handle_partial_results(audio_chunks: AsyncIterable[bytes]) -> AsyncGenerator[Dict[str, Any], None]:
    client = get_speech_client()
    options = get_live_options(interim_results=True)
    transcript_queue = asyncio.Queue()
    connection = client.listen.live.v("1", options)

    def on_transcript(result):
        try:
            transcript_obj = result.channel.alternatives[0]
            transcript = transcript_obj.transcript
            is_final = getattr(result, 'is_final', False) or getattr(transcript_obj, 'is_final', False)
            if transcript.strip():
                event = {'transcript': transcript, 'is_final': is_final}
                loop = asyncio.get_event_loop()
                loop.call_soon_threadsafe(transcript_queue.put_nowait, event)
        except Exception:
            pass

    connection.on(LiveTranscriptionEvents.Transcript, on_transcript)
    connection.start()

    async def sender():
        async for chunk in audio_chunks:
            connection.send(chunk)

    sender_task = asyncio.create_task(sender())

    try:
        while True:
            yield await transcript_queue.get()
    finally:
        sender_task.cancel()
        try:
            await sender_task
        except asyncio.CancelledError:
            pass
        connection.finish()
