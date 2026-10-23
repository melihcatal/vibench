from typing import AsyncIterable, AsyncIterator

from deepgram import LiveTranscriptionEvents

from speech_client import base_options, create_client, load_speech_config
from speech_models import event_from_deepgram


async def stream_audio_chunks(source: AsyncIterable[bytes]) -> AsyncIterator[str]:
    config = load_speech_config()
    client = create_client(config)
    dg_stream = await client.listen.asyncwebsocket.v("1")
    results = []

    def on_message(_, payload, **__):
        event = event_from_deepgram(payload)
        if event.text:
            results.append(event.text)

    dg_stream.on(LiveTranscriptionEvents.Transcript, on_message)
    await dg_stream.start(base_options(config))
    async for chunk in source:
        await dg_stream.send(chunk)
        while results:
            yield results.pop(0)
