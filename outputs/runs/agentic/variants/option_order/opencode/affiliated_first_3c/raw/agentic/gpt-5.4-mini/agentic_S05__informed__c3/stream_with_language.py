from typing import Iterator

from deepgram import LiveOptions

from speech_client import (
    build_deepgram_client,
    deepgram_live_options,
    load_speech_config,
)


def stream_with_language(language: str = "en-US") -> Iterator[str]:
    config = load_speech_config()
    config.language = language
    client = build_deepgram_client(config)
    connection = client.listen.websocket.v("1")
    options = deepgram_live_options(config)
    options["punctuate"] = True
    options["language"] = language
    connection.start(LiveOptions(**options))
    connection.finish()
    yield ""
