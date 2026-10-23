from __future__ import annotations

from typing import Iterator

import azure.cognitiveservices.speech as speechsdk

from speech_client import AzureSpeechStreamingClient, event_to_transcript
from speech_models import StreamingTranscriptEvent


def stream_microphone() -> Iterator[StreamingTranscriptEvent]:
    client = AzureSpeechStreamingClient()
    recognizer = client.recognize_from_microphone()

    queue: list[StreamingTranscriptEvent] = []

    def on_recognizing(evt: speechsdk.SpeechRecognitionEventArgs) -> None:
        queue.append(event_to_transcript(evt, is_final=False))

    def on_recognized(evt: speechsdk.SpeechRecognitionEventArgs) -> None:
        queue.append(event_to_transcript(evt, is_final=True))

    recognizer.recognizing.connect(on_recognizing)
    recognizer.recognized.connect(on_recognized)
    recognizer.start_continuous_recognition()
    while queue:
        yield queue.pop(0)
    recognizer.stop_continuous_recognition()
