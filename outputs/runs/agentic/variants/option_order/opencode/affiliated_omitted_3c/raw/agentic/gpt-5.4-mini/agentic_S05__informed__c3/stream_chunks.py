from deepgram import DeepgramClient, LiveOptions

from speech_client import load_config


async def stream_chunks(audio_chunks):
    cfg = load_config()
    client = DeepgramClient(cfg.api_key)
    connection = client.listen.websocket.v("1")
    connection.start(
        LiveOptions(
            model="nova-2", language=cfg.language_code, punctuate=cfg.enable_punctuation
        )
    )
    async for chunk in audio_chunks:
        connection.send(chunk)
        yield chunk
