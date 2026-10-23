from typing import AsyncIterable, AsyncIterator

from deepgram import LiveTranscriptionEvents

from speech_client import build_live_options, create_deepgram_client
from speech_models import AudioChunk, TranscriptEvent, normalize_text


async def stream_chunks(
    chunks: AsyncIterable[AudioChunk],
) -> AsyncIterator[TranscriptEvent]:
    client = create_deepgram_client()
    conn = await client.listen.asynclive.v("1")
    results = []

    def on_message(_, result, **__):
        alt = result.channel.alternatives[0]
        results.append(
            TranscriptEvent(
                text=normalize_text(alt.transcript),
                is_final=bool(result.channel.is_final),
                confidence=getattr(alt, "confidence", None),
            )
        )

    conn.on(LiveTranscriptionEvents.Transcript, on_message)
    await conn.start(build_live_options())
    async for chunk in chunks:
        await conn.send(chunk.data)
        for item in results:
            yield item
        results.clear()
    await conn.finish()
