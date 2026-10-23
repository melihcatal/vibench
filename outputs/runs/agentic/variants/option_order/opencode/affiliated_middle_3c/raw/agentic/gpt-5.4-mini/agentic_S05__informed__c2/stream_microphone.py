import asyncio
from typing import AsyncIterator, Iterator

import pyaudio
from deepgram import LiveTranscriptionEvents

from speech_client import base_options, create_client, load_speech_config
from speech_models import event_from_deepgram


async def microphone_audio_stream(chunk_size: int = 1024) -> AsyncIterator[bytes]:
    pa = pyaudio.PyAudio()
    stream = pa.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=16000,
        input=True,
        frames_per_buffer=chunk_size,
    )
    try:
        while True:
            data = await asyncio.to_thread(
                stream.read, chunk_size, exception_on_overflow=False
            )
            yield data
    finally:
        stream.stop_stream()
        stream.close()
        pa.terminate()


async def stream_microphone() -> AsyncIterator[str]:
    config = load_speech_config()
    client = create_client(config)
    dg_stream = await client.listen.asyncwebsocket.v("1")
    transcripts: asyncio.Queue[str] = asyncio.Queue()

    def on_message(_, payload, **__):
        event = event_from_deepgram(payload)
        if event.text:
            transcripts.put_nowait(event.text)

    dg_stream.on(LiveTranscriptionEvents.Transcript, on_message)
    await dg_stream.start(base_options(config))
    async for audio in microphone_audio_stream():
        await dg_stream.send(audio)
        while not transcripts.empty():
            yield await transcripts.get()
