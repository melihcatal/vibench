from typing import AsyncIterable, AsyncIterator

from deepgram import LiveOptions

from speech_client import deepgram_client, load_speech_config
from speech_models import normalize_transcript


async def stream_chunks(source: AsyncIterable[bytes]) -> AsyncIterator[str]:
    cfg = load_speech_config()
    client = deepgram_client()
    messages = []

    def on_message(_, result, **__):
        channel = getattr(result, "channel", None)
        if channel and getattr(channel, "alternatives", None):
            messages.append(
                normalize_transcript(
                    {
                        "text": channel.alternatives[0].transcript,
                        "is_final": getattr(result, "is_final", False),
                    }
                )
            )

    dg = client.listen.websocket.v("1")
    dg.on("Transcript", on_message)
    dg.start(
        LiveOptions(
            model="nova-2",
            language=cfg.language,
            punctuate=cfg.punctuate,
            interim_results=True,
        )
    )
    async for chunk in source:
        dg.send(chunk)
        while messages:
            yield messages.pop(0).text
    dg.finish()
