from typing import Iterator

import azure.cognitiveservices.speech as speechsdk

from speech_client import create_speech_config
from speech_models import TranscriptEvent, normalize_event


def stream_microphone() -> Iterator[TranscriptEvent]:
    speech_config = create_speech_config()
    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
    recognizer = speechsdk.SpeechRecognizer(
        speech_config=speech_config, audio_config=audio_config
    )
    queue = []

    def _on_recognizing(evt):
        queue.append(
            TranscriptEvent(
                text=normalize_event(evt.result).text,
                is_final=False,
                confidence=getattr(evt.result, "confidence", None),
            )
        )

    recognizer.recognizing.connect(_on_recognizing)
    recognizer.start_continuous_recognition()
    while queue:
        yield queue.pop(0)
