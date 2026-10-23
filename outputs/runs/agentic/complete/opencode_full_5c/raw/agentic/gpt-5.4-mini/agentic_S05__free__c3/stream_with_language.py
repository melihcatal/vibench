import json
from typing import AsyncIterator

import websockets

from speech_client import load_config
from speech_models import TranscriptEvent, normalize_transcript


async def stream_with_language(
    language_code: str = "en", punctuate: bool = True
) -> AsyncIterator[TranscriptEvent]:
    config = load_config()
    async with websockets.connect(
        config.assemblyai_realtime_url,
        extra_headers={"Authorization": config.assemblyai_api_key},
    ) as ws:
        await ws.send(
            json.dumps(
                {
                    "sample_rate": 16000,
                    "language_code": language_code,
                    "punctuate": punctuate,
                }
            )
        )
        while True:
            payload = json.loads(await ws.recv())
            event = normalize_transcript(payload)
            if event.text:
                yield event
