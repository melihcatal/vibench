import os

from deepgram import DeepgramClient, LiveOptions

from speech_client import load_speech_config


def stream_with_language(language: str | None = None, punctuation: bool = True):
    config = load_speech_config()
    client = DeepgramClient(config.api_key or os.environ["DEEPGRAM_API_KEY"])
    conn = client.listen.websocket.v("1")
    conn.start(
        LiveOptions(
            model="nova-2",
            language=language or config.language,
            smart_format=punctuation,
            interim_results=True,
        )
    )
    return conn
