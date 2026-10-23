from __future__ import annotations

from typing import Generator

from speech_client import DeepgramSpeechClient, SpeechConfig
from speech_models import StreamingUtterance


def stream_with_language(language: str = "en-US", punctuation: bool = True) -> Generator[StreamingUtterance, None, None]:
    from deepgram import LiveTranscriptionEvents  # provider-identifying import
    import pyaudio

    config = SpeechConfig.from_env()
    config = SpeechConfig(api_key=config.api_key, language=language, punctuation=punctuation, model=config.model)
    client = DeepgramSpeechClient(config)

    audio = pyaudio.PyAudio()
    stream = audio.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=3200)
    live = client.client().listen.websocket.v("1")
    queue: list[StreamingUtterance] = []

    def on_message(_, result, **__):
        utterance = client.transcribe_event(result)
        if utterance.text:
            queue.append(utterance)

    live.on(LiveTranscriptionEvents.Transcript, on_message)
    live.start(client.live_options())
    try:
        while True:
            live.send(stream.read(3200, exception_on_overflow=False))
            while queue:
                yield queue.pop(0)
    finally:
        live.finish()
        stream.stop_stream()
        stream.close()
        audio.terminate()
