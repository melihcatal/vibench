import asyncio
import pyaudio
from typing import AsyncGenerator
from deepgram import DeepgramClient, LiveOptions, LiveTranscriptionEvents
from speech_client import get_speech_client, get_live_options
from speech_models import prepare_audio_chunk

async def stream_microphone() -> AsyncGenerator[str, None]:
    client = get_speech_client()
    options = get_live_options()
    queue = asyncio.Queue()
    connection = client.listen.live.v('1')

    def on_transcript(result):
        transcript = ''
        if hasattr(result, 'channel') and result.channel and hasattr(result.channel, 'alternatives') and result.channel.alternatives:
            transcript = result.channel.alternatives[0].transcript or ''
        if transcript:
            asyncio.get_event_loop().call_soon_threadsafe(queue.put_nowait, transcript)

    connection.on(LiveTranscriptionEvents.Transcript, on_transcript)

    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1280)

    loop = asyncio.get_running_loop()

    async def send_audio():
        while True:
            data = await loop.run_in_executor(None, stream.read, 1280, False)
            connection.send(prepare_audio_chunk(data))

    send_task = asyncio.create_task(send_audio())

    try:
        connection.start(options)
        while True:
            transcript = await queue.get()
            yield transcript
    finally:
        send_task.cancel()
        stream.stop_stream()
        stream.close()
        p.terminate()
        connection.finish()