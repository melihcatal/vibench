import asyncio
import os
from deepgram import DeepgramClient, LiveTranscriptionEvents, LiveOptions, PrerecordedOptions
from speech_models import parse_live_result, Transcript

DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")
if not DEEPGRAM_API_KEY:
    raise ValueError("DEEPGRAM_API_KEY environment variable is required.")

client = DeepgramClient(DEEPGRAM_API_KEY)

async def stream_chunks(audio_chunk_generator):
    options = LiveOptions(
        model="nova-2",
        language="en-US",
        punctuate=True,
        interim_results=True,
    )
    
    connection = client.listen.live.v("1")
    transcript_queue = asyncio.Queue()
    
    def on_transcript(result):
        parsed = parse_live_result(result)
        if parsed:
            asyncio.create_task(transcript_queue.put(parsed))
    
    def on_close(_):
        asyncio.create_task(transcript_queue.put(None))
    
    connection.on(LiveTranscriptionEvents.Transcript, on_transcript)
    connection.on(LiveTranscriptionEvents.Close, on_close)
    
    await connection.open(options=options)
    
    async def send_chunks():
        try:
            async for chunk in audio_chunk_generator:
                await connection.send(chunk)
        except asyncio.CancelledError:
            pass
        finally:
            await connection.finish()
    
    send_task = asyncio.create_task(send_chunks())
    
    try:
        while True:
            transcript = await transcript_queue.get()
            if transcript is None:
                break
            yield transcript.text, transcript.is_final
    finally:
        send_task.cancel()