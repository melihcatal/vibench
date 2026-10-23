from __future__ import annotations

from typing import Any, AsyncIterable, AsyncIterator

from speech_client import OPENAI_REALTIME_MODEL, get_openai_client, pcm16_bytes_to_base64, realtime_session_config
from speech_models import StreamingConfig, StreamingTranscriptEvent
from partial_results import iter_transcript_events


async def stream_audio_chunks(
    audio_source: AsyncIterable[bytes],
    config: StreamingConfig | None = None,
    api_key: str | None = None,
) -> AsyncIterator[StreamingTranscriptEvent]:
    client = get_openai_client(api_key)
    async with client.beta.realtime.connect(model=OPENAI_REALTIME_MODEL) as connection:
        await connection.send(realtime_session_config(config))

        async for chunk in audio_source:
            if not chunk:
                continue
            await connection.send(
                {
                    "type": "input_audio_buffer.append",
                    "audio": pcm16_bytes_to_base64(chunk),
                }
            )

        await connection.send({"type": "input_audio_buffer.commit"})
        await connection.send({"type": "response.create"})

        async for transcript_event in iter_transcript_events(connection):
            yield transcript_event
