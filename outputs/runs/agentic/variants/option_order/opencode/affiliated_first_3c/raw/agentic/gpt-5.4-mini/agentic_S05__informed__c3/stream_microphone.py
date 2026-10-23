from typing import Iterator

import pyaudio
from deepgram import LiveOptions

from speech_client import (
    attach_transcript_handler,
    build_deepgram_client,
    deepgram_live_options,
    load_speech_config,
)


def stream_microphone() -> Iterator[str]:
    config = load_speech_config()
    client = build_deepgram_client(config)
    connection = client.listen.websocket.v("1")
    attach_transcript_handler(connection, lambda transcript, _: None)
    connection.start(LiveOptions(**deepgram_live_options(config)))
    audio = pyaudio.PyAudio()
    stream = audio.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=16000,
        input=True,
        frames_per_buffer=1024,
    )
    try:
        while True:
            chunk = stream.read(1024)
            connection.send(chunk)
            yield ""
    finally:
        stream.stop_stream()
        stream.close()
        audio.terminate()
        connection.finish()
