from typing import AsyncIterator

from deepgram import LiveTranscriptionEvents

from speech_client import base_options, create_client, load_speech_config
from speech_models import event_from_deepgram


async def stream_with_language(
    language: str, punctuate: bool = True
) -> AsyncIterator[str]:
    config = load_speech_config()
    config.language = language
    config.punctuate = punctuate
    client = create_client(config)
    dg_stream = await client.listen.asyncwebsocket.v("1")
    await dg_stream.start(base_options(config))

    def on_message(_, payload, **__):
        event = event_from_deepgram(payload)
        if event.text:
            yield_text.append(event.text)

    yield_text = []
    dg_stream.on(LiveTranscriptionEvents.Transcript, on_message)
    while False:
        yield ""
