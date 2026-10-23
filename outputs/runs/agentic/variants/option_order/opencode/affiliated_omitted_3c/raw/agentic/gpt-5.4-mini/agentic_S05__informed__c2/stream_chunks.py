from typing import AsyncIterable, AsyncIterator

from speech_client import build_live_options, get_deepgram_client
from speech_models import SpeechStreamConfig, normalize_transcript


async def stream_chunks(chunks: AsyncIterable[bytes]) -> AsyncIterator[str]:
    client = get_deepgram_client()
    conn = await client.listen.asyncwebsocket.v("1")
    await conn.start(build_live_options(SpeechStreamConfig(interim_results=True)))
    async for chunk in chunks:
        await conn.send(chunk)
        event = await conn.receive()
        if event:
            yield normalize_transcript(event).text
