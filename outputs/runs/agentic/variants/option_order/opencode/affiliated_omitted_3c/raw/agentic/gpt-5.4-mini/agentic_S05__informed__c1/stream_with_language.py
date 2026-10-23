from deepgram import DeepgramClient, LiveOptions

from speech_client import load_speech_config


def start_streaming_recognizer(
    language_code: str | None = None, punctuation: bool | None = None
):
    config = load_speech_config()
    client = DeepgramClient(config.api_key)
    return client.listen.asyncwebsocket.v("1").start(
        LiveOptions(
            model="nova-2",
            language=language_code or config.language_code,
            punctuate=config.punctuation if punctuation is None else punctuation,
            interim_results=True,
        )
    )
