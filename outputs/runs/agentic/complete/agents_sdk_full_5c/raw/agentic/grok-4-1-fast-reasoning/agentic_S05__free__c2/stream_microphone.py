import asyncio
import os
import pyaudio
from deepgram import DeepgramClient, LiveTranscriptionEvents, LiveOptions
from speech_client import setup_microphone, close_microphone, get_audio_config
from speech_models import parse_live_result, Transcript

DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")
if not DEEPGRAM_API_KEY:
    raise ValueError("DEEPGRAM_API_KEY environment variable is required.")

client = DeepgramClient(DEEPGRAM_API_KEY)

async def stream_microphone():
    p, stream = setup_microphone()
    chunk_size = get_audio_config()["frames_per_buffer"]
    
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
    
    async def send_audio():
        try:
            while True:
                data = stream.read(chunk_size, exception_on_overflow=False)
                await connection.send(data)
        except asyncio.CancelledError:
            pass
        finally:
            await connection.finish()
    
    send_task = asyncio.create_task(send_audio())
    
    try:
        while True:
            transcript = await transcript_queue.get()
            if transcript is None:
                break
            yield transcript.text, transcript.is_final
    finally:
        send_task.cancel()
        close_microphone(p, stream)