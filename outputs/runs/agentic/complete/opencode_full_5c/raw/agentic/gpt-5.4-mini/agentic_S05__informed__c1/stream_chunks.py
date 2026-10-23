import os

from deepgram import DeepgramClient, LiveOptions

from speech_models import TranscriptChunk
from speech_client import load_speech_config


async def stream_chunks(source):
    config = load_speech_config()
    client = DeepgramClient(config.api_key or os.environ["DEEPGRAM_API_KEY"])
    conn = client.listen.websocket.v("1")
    conn.start(
        LiveOptions(
            model="nova-2",
            language=config.language,
            smart_format=config.enable_punctuation,
        )
    )
    async for chunk in source:
        if isinstance(chunk, TranscriptChunk):
            conn.send(chunk.audio)
        else:
            conn.send(chunk)
    conn.finish()
