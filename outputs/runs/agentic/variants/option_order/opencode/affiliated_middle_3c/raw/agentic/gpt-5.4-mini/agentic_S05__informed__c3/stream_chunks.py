from typing import AsyncIterator, Iterable

from deepgram import DeepgramClient, LiveOptions

from speech_client import load_config, build_deepgram_options
from speech_models import TranscriptEvent, normalize_text


async def stream_chunks(chunks: AsyncIterator[bytes]) -> AsyncIterator[TranscriptEvent]:
    config = load_config()
    client = DeepgramClient(config.deepgram_api_key)
    async with client.listen.asyncwebsocket.v("1") as ws:
        await ws.start(LiveOptions(**build_deepgram_options(config)))
        async for chunk in chunks:
            await ws.send(chunk)
        await ws.finish()
        async for result in ws:
            alt = result.channel.alternatives[0]
            yield TranscriptEvent(
                normalize_text(alt.transcript), result.is_final, config.language
            )
