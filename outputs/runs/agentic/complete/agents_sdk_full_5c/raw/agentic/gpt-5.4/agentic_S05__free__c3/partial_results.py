from __future__ import annotations

from typing import Callable, Optional

import azure.cognitiveservices.speech as speechsdk

from speech_models import TranscriptEvent, normalize_transcript_text


class PartialResultHandler:
    def __init__(self, on_event: Optional[Callable[[TranscriptEvent], None]] = None) -> None:
        self.on_event = on_event
        self.latest_partial: str = ""
        self.finalized: list[str] = []

    def handle_recognizing(self, evt: speechsdk.SpeechRecognitionEventArgs) -> TranscriptEvent:
        text = normalize_transcript_text(evt.result.text)
        event = TranscriptEvent(
            text=text,
            is_final=False,
            stability=None,
            confidence=None,
            raw=evt.result,
        )
        self.latest_partial = text
        if self.on_event:
            self.on_event(event)
        return event

    def handle_recognized(self, evt: speechsdk.SpeechRecognitionEventArgs) -> Optional[TranscriptEvent]:
        if evt.result.reason != speechsdk.ResultReason.RecognizedSpeech:
            return None
        text = normalize_transcript_text(evt.result.text)
        event = TranscriptEvent(
            text=text,
            is_final=True,
            stability=1.0,
            confidence=None,
            raw=evt.result,
        )
        self.latest_partial = ""
        if text:
            self.finalized.append(text)
        if self.on_event:
            self.on_event(event)
        return event

    def bind(self, recognizer: speechsdk.SpeechRecognizer) -> None:
        recognizer.recognizing.connect(self.handle_recognizing)
        recognizer.recognized.connect(self.handle_recognized)

    def current_transcript(self) -> str:
        base = " ".join(self.finalized)
        if self.latest_partial:
            return f"{base} {self.latest_partial}".strip()
        return base.strip()
