from __future__ import annotations

from typing import Generator

from speech_client import DeepgramSpeechClient
from speech_models import StreamingUtterance


def stream_microphone() -> Generator[StreamingUtterance, None, None]:
    from deepgram import LiveTranscriptionEvents  # provider-identifying import
    import pyaudio

    client = DeepgramSpeechClient()
    audio = pyaudio.PyAudio()
    stream = audio.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=3200)

    live = client.client().listen.websocket.v("1")
    options = client.live_options()

    def on_message(_, result, **__):
        utterance = client.transcribe_event(result)
        if utterance.text:
            queue.append(utterance)

    queue: list[StreamingUtterance] = []
    live.on(LiveTranscriptionEvents.Transcript, on_message)
    live.start(options)
    try:
        while True:
            data = stream.read(3200, exception_on_overflow=False)
            live.send(data)
            while queue:
                yield queue.pop(0)
    finally:
        live.finish()
        stream.stop_stream()
        stream.close()
        audio.terminate()
