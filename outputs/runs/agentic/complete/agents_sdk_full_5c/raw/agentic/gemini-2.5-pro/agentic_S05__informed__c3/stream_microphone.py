import asyncio
from typing import AsyncGenerator
from deepgram import LiveTranscriptionEvents
from speech_client import get_speech_client, get_live_options

# Placeholder for a real microphone audio stream
async def get_microphone_audio_stream() -> AsyncGenerator[bytes, None]:
    for _ in range(5):
        yield b'\x00' * 3200
        await asyncio.sleep(0.1)

async def stream_from_microphone() -> AsyncGenerator[str, None]:
    """Streams audio from a microphone and yields transcripts from a queue."""
    deepgram_client = get_speech_client()
    options = get_live_options(interim_results=True)
    
    transcript_queue = asyncio.Queue()

    try:
        dg_connection = deepgram_client.listen.asynclive.v("1")

        async def on_message(self, result, **kwargs):
            transcript = result.channel.alternatives[0].transcript
            if transcript:
                await transcript_queue.put(transcript)

        async def on_close(self, **kwargs):
            await transcript_queue.put(None) # Signal end of stream

        dg_connection.on(LiveTranscriptionEvents.Transcript, on_message)
        dg_connection.on(LiveTranscriptionEvents.Close, on_close)

        await dg_connection.start(options)

        # Start sending audio in a separate task
        async def sender():
            async for chunk in get_microphone_audio_stream():
                if chunk:
                    await dg_connection.send(chunk)
            await dg_connection.finish()

        sender_task = asyncio.create_task(sender())

        # Yield transcripts from the queue
        while True:
            transcript = await transcript_queue.get()
            if transcript is None:
                break
            yield transcript
        
        await sender_task

    except Exception as e:
        print(f"Could not open stream: {e}")
