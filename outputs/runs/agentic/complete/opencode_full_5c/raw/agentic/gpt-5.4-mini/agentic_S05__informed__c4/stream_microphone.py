import asyncio
from typing import AsyncIterator

import pyaudio
from deepgram import LiveTranscriptionEvents

from speech_client import build_live_options, create_deepgram_client, load_speech_config
from speech_models import TranscriptEvent, normalize_text


async def stream_microphone() -> AsyncIterator[TranscriptEvent]:
    client = create_deepgram_client(load_speech_config())
    conn = await client.listen.asynclive.v("1")
    queue: asyncio.Queue[TranscriptEvent] = asyncio.Queue()

    def on_message(_, result, **__):
        channel = result.channel
        alt = channel.alternatives[0]
        queue.put_nowait(
            TranscriptEvent(
                text=normalize_text(alt.transcript),
                is_final=bool(channel.is_final),
                confidence=getattr(alt, "confidence", None),
            )
        )

    conn.on(LiveTranscriptionEvents.Transcript, on_message)
    await conn.start(build_live_options())
    pa = pyaudio.PyAudio()
    stream = pa.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=16000,
        input=True,
        frames_per_buffer=3200,
    )
    try:
        while True:
            data = stream.read(3200, exception_on_overflow=False)
            await conn.send(data)
            while not queue.empty():
                yield queue.get_nowait()
    finally:
        stream.stop_stream()
        stream.close()
        pa.terminate()
        await conn.finish()
