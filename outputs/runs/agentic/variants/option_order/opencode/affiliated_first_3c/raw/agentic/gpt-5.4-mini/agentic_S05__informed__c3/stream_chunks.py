from typing import AsyncIterator, Iterator

from deepgram import LiveOptions

from speech_client import (
    attach_transcript_handler,
    build_deepgram_client,
    deepgram_live_options,
    load_speech_config,
)


async def stream_chunks(source: AsyncIterator[bytes]) -> AsyncIterator[str]:
    config = load_speech_config()
    client = build_deepgram_client(config)
    connection = client.listen.websocket.v("1")
    attach_transcript_handler(connection, lambda transcript, _: None)
    connection.start(LiveOptions(**deepgram_live_options(config)))
    async for chunk in source:
        connection.send(chunk)
        yield ""
    connection.finish()
