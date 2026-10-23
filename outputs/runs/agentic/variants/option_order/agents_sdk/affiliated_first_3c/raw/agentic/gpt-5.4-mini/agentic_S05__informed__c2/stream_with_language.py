from __future__ import annotations

from typing import Iterator

import azure.cognitiveservices.speech as speechsdk

from speech_client import SpeechConfig, load_speech_config, stream_events_from_recognizer
from speech_models import TranscriptEvent


def stream_with_language(language: str, enable_punctuation: bool = True) -> Iterator[TranscriptEvent]:
    base = load_speech_config()
    cfg = SpeechConfig(key=base.key, region=base.region, language=language, enable_punctuation=enable_punctuation)
    speech_config = speechsdk.SpeechConfig(subscription=cfg.key, region=cfg.region)
    speech_config.speech_recognition_language = cfg.language
    if cfg.enable_punctuation:
        speech_config.set_property(speechsdk.PropertyId.SpeechServiceResponse_PostProcessingOption, "TrueText")
    recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=speechsdk.audio.AudioConfig(use_default_microphone=True))
    yield from stream_events_from_recognizer(recognizer)
