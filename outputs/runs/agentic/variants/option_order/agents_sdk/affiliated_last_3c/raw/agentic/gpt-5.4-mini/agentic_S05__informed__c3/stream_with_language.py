from __future__ import annotations

from typing import Iterator, Optional

from deepgram import DeepgramClient, LiveOptions, LiveTranscriptionEvents

from speech_client import DeepgramSpeechClient, SpeechConfig
from speech_models import TranscriptEvent


class LanguageAwareStreamer:
    def __init__(self, language: str = "en-US", punctuate: bool = True) -> None:
        config = SpeechConfig(api_key=__import__("os").environ["DEEPGRAM_API_KEY"], language=language, punctuate=punctuate)
        self.client = DeepgramSpeechClient(config)
        self.dg = self.client.client

    def start(self) -> Iterator[TranscriptEvent]:
        conn = self.dg.listen.websocket.v("1")
        options = LiveOptions(**self.client._options())
        queue: list[TranscriptEvent] = []

        def on_message(_, result, **__):
            queue.append(self.client.process_event(result.to_dict()))

        conn.on(LiveTranscriptionEvents.Transcript, on_message)
        conn.start(options)
        while queue:
            yield queue.pop(0)
        conn.finish()
