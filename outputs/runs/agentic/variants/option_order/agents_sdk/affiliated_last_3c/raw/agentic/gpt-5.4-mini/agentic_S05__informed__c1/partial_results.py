from __future__ import annotations

from typing import AsyncIterator

from speech_models import StreamingTranscript, normalize_transcript
from speech_client import SpeechConfig, build_live_options, create_deepgram_client


async def partial_results(audio_source) -> AsyncIterator[StreamingTranscript]:
    config = SpeechConfig.from_env()
    client = create_deepgram_client(config)
    connection = await client.listen.asyncwebsocket.v("1")
    connection.on("Transcript", lambda message: None)
    await connection.start(build_live_options(config, interim_results=True))

    try:
        async for chunk in audio_source:
            await connection.send(chunk)
            event = await connection.recv()
            transcript = normalize_transcript(event)
            if transcript.text:
                yield transcript
    finally:
        await connection.finish()
