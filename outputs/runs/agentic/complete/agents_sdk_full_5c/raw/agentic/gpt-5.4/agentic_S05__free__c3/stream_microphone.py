from __future__ import annotations

from collections.abc import Iterator
from queue import Queue
from typing import Optional

import azure.cognitiveservices.speech as speechsdk

from partial_results import PartialResultHandler
from speech_client import create_speech_recognizer
from speech_models import StreamingRecognitionConfig, TranscriptEvent


class MicrophoneTranscriptStream:
    def __init__(self, config: Optional[StreamingRecognitionConfig] = None) -> None:
        self.config = config or StreamingRecognitionConfig()
        self.recognizer = create_speech_recognizer(self.config)
        self._queue: Queue[TranscriptEvent] = Queue()
        self._handler = PartialResultHandler(on_event=self._queue.put)
        self._handler.bind(self.recognizer)
        self._stopped = False
        self.recognizer.session_stopped.connect(self._on_session_stopped)
        self.recognizer.canceled.connect(self._on_canceled)

    def _on_session_stopped(self, evt: speechsdk.SessionEventArgs) -> None:
        self._stopped = True

    def _on_canceled(self, evt: speechsdk.SpeechRecognitionCanceledEventArgs) -> None:
        self._stopped = True

    def transcripts(self) -> Iterator[TranscriptEvent]:
        self.recognizer.start_continuous_recognition()
        try:
            while not self._stopped or not self._queue.empty():
                event = self._queue.get(timeout=0.25)
                if self.config.interim_results or event.is_final:
                    yield event
        except Exception:
            return
        finally:
            self.recognizer.stop_continuous_recognition()
