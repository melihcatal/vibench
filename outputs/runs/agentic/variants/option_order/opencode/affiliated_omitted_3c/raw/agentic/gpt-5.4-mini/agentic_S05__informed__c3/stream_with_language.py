from deepgram import DeepgramClient, LiveOptions

from speech_client import load_config


def stream_with_language(audio_source, language_code: str | None = None):
    cfg = load_config()
    client = DeepgramClient(cfg.api_key)
    connection = client.listen.websocket.v("1")
    connection.start(
        LiveOptions(
            model="nova-2", language=language_code or cfg.language_code, punctuate=True
        )
    )
    for chunk in audio_source:
        connection.send(chunk)
        yield chunk
