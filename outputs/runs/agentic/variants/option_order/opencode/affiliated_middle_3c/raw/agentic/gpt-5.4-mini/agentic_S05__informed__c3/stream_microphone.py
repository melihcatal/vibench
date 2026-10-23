import asyncio
from typing import AsyncIterator

from deepgram import DeepgramClient, LiveTranscriptionEvents, LiveOptions

from speech_client import load_config, build_deepgram_options
from speech_models import TranscriptEvent, normalize_text


async def stream_microphone() -> AsyncIterator[TranscriptEvent]:
    config = load_config()
    client = DeepgramClient(config.deepgram_api_key)
    options = LiveOptions(**build_deepgram_options(config))
    async with client.listen.asyncwebsocket.v("1") as ws:
        await ws.start(options)

        async def on_message(result, **kwargs):
            alt = result.channel.alternatives[0]
            await queue.put(
                TranscriptEvent(
                    normalize_text(alt.transcript), not result.is_final, config.language
                )
            )

        queue: asyncio.Queue[TranscriptEvent] = asyncio.Queue()
        ws.on(LiveTranscriptionEvents.Transcript, on_message)
        while True:
            event = await queue.get()
            yield event
