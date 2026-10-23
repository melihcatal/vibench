from typing import AsyncIterable, AsyncIterator

from speech_client import build_live_options, get_deepgram_client
from speech_models import SpeechStreamConfig, normalize_transcript


async def stream_with_language(
    chunks: AsyncIterable[bytes], language_code: str, punctuation: bool = True
) -> AsyncIterator[str]:
    client = get_deepgram_client()
    config = SpeechStreamConfig(
        language_code=language_code,
        punctuation=punctuation,
        interim_results=True,
        model="nova-2",
    )
    conn = await client.listen.asyncwebsocket.v("1")
    await conn.start(build_live_options(config))
    async for chunk in chunks:
        await conn.send(chunk)
        event = await conn.receive()
        if event:
            yield normalize_transcript(event).text
