from __future__ import annotations

from typing import Iterator

import azure.cognitiveservices.speech as speechsdk

from speech_client import AzureSpeechStreamingClient
from speech_models import TranscriptChunk


def stream_microphone() -> Iterator[TranscriptChunk]:
    client = AzureSpeechStreamingClient()
    recognizer = client.recognizer()
    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
    recognizer.audio_config = audio_config

    def on_recognizing(evt: speechsdk.SpeechRecognitionEventArgs) -> None:
        text = evt.result.text.strip()
        if text:
            yield_chunk = TranscriptChunk(text=text, is_final=False, metadata={"provider": "azure-speech"})
            stream_microphone._pending.append(yield_chunk)  # type: ignore[attr-defined]

    def on_recognized(evt: speechsdk.SpeechRecognitionEventArgs) -> None:
        text = evt.result.text.strip()
        if text:
            yield_chunk = TranscriptChunk(text=text, is_final=True, metadata={"provider": "azure-speech"})
            stream_microphone._pending.append(yield_chunk)  # type: ignore[attr-defined]

    stream_microphone._pending = []  # type: ignore[attr-defined]
    recognizer.recognizing.connect(on_recognizing)
    recognizer.recognized.connect(on_recognized)
    recognizer.start_continuous_recognition_async().get()
    while True:
        if stream_microphone._pending:  # type: ignore[attr-defined]
            yield stream_microphone._pending.pop(0)  # type: ignore[attr-defined]
        else:
            break
    recognizer.stop_continuous_recognition_async().get()
