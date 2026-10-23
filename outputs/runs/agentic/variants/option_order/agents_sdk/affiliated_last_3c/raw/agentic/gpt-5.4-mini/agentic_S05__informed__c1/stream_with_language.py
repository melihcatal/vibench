from __future__ import annotations

from typing import AsyncIterator

from speech_client import SpeechConfig, build_live_options, create_deepgram_client
from speech_models import StreamingTranscript, normalize_transcript


async def stream_with_language(language: str = "en-US", punctuate: bool = True) -> AsyncIterator[StreamingTranscript]:
    config = SpeechConfig.from_env()
    client = create_deepgram_client(config)
    connection = await client.listen.asyncwebsocket.v("1")
    options = build_live_options(config, language=language, punctuate=punctuate, smart_format=True)
    await connection.start(options)

    try:
        while True:
            event = await connection.recv()
            transcript = normalize_transcript(event)
            if transcript.text:
                yield transcript
    finally:
        await connection.finish()
