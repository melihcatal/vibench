import asyncio
from typing import AsyncGenerator
from deepgram import DeepgramClient, LiveOptions, LiveTranscriptionEvents
from speech_client import get_speech_client, get_live_options
from speech_models import prepare_audio_chunk

async def stream_with_language(
    audio_source: AsyncGenerator[bytes, None],
    language: str = 'en-US',
    punctuate: bool = True
) -> AsyncGenerator[str, None]:
    client = get_speech_client()
    options = get_live_options(language=language, punctuate=punctuate)
    queue = asyncio.Queue()
    connection = client.listen.live.v('1')

    def on_transcript(result):
        transcript = ''
        if hasattr(result, 'channel') and result.channel and hasattr(result.channel, 'alternatives') and result.channel.alternatives:
            transcript = result.channel.alternatives[0].transcript or ''
        if transcript:
            asyncio.get_event_loop().call_soon_threadsafe(queue.put_nowait, transcript)

    connection.on(LiveTranscriptionEvents.Transcript, on_transcript)

    loop = asyncio.get_running_loop()

    async def process_source():
        async for chunk in audio_source:
            connection.send(prepare_audio_chunk(chunk))

    process_task = asyncio.create_task(process_source())

    try:
        connection.start(options)
        while True:
            transcript = await queue.get()
            yield transcript
    finally:
        process_task.cancel()
        connection.finish()