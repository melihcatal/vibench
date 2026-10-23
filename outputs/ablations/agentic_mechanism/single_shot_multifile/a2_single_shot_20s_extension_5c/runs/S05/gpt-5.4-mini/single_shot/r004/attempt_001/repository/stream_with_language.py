import asyncio
from typing import AsyncIterator

from deepgram import LiveOptions

from speech_client import build_deepgram_client, load_speech_config
from speech_models import TranscriptEvent, normalize_transcript_event


async def stream_with_language(language: str = "en-US", punctuate: bool = True) -> AsyncIterator[TranscriptEvent]:
    config = load_speech_config()
    client = build_deepgram_client()
    connection = client.listen.websocket.v("1")
    options = LiveOptions(
        model=config.model,
        language=language,
        punctuate=punctuate,
        interim_results=True,
        smart_format=True,
    )
    await connection.start(options)
    try:
        while True:
            message = await connection.recv()
            event = normalize_transcript_event(message)
            if event is not None:
                yield event
    finally:
        await connection.finish()

