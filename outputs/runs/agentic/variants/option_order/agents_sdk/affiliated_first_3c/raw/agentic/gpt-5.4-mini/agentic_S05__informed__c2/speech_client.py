from __future__ import annotations

import os
from dataclasses import dataclass
from typing import AsyncIterable, Iterable, Iterator, Optional

import azure.cognitiveservices.speech as speechsdk

from speech_models import StreamingAudioChunk, TranscriptEvent


@dataclass
class SpeechConfig:
    key: str
    region: str
    language: str = "en-US"
    enable_punctuation: bool = True


def load_speech_config() -> SpeechConfig:
    return SpeechConfig(
        key=os.environ["AZURE_SPEECH_KEY"],
        region=os.environ["AZURE_SPEECH_REGION"],
        language=os.getenv("AZURE_SPEECH_LANGUAGE", "en-US"),
        enable_punctuation=os.getenv("AZURE_SPEECH_ENABLE_PUNCTUATION", "true").lower() == "true",
    )


def build_recognizer(config: Optional[SpeechConfig] = None) -> speechsdk.SpeechRecognizer:
    cfg = config or load_speech_config()
    speech_config = speechsdk.SpeechConfig(subscription=cfg.key, region=cfg.region)
    speech_config.speech_recognition_language = cfg.language
    if cfg.enable_punctuation:
        speech_config.set_property(speechsdk.PropertyId.SpeechServiceResponse_PostProcessingOption, "TrueText")
    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
    return speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)


def stream_events_from_recognizer(recognizer: speechsdk.SpeechRecognizer) -> Iterator[TranscriptEvent]:
    def _make_event(evt, is_final: bool) -> TranscriptEvent:
        return TranscriptEvent(text=evt.result.text, is_final=is_final, confidence=getattr(evt.result, "confidence", None), language=getattr(evt.result, "language", None), raw={"reason": str(evt.result.reason)})

    queue: list[TranscriptEvent] = []

    recognizer.recognizing.connect(lambda evt: queue.append(_make_event(evt, False)))
    recognizer.recognized.connect(lambda evt: queue.append(_make_event(evt, True)))
    recognizer.start_continuous_recognition()
    try:
        while True:
            while queue:
                yield queue.pop(0)
    finally:
        recognizer.stop_continuous_recognition()


async def iter_streaming_chunks(source: AsyncIterable[bytes]) -> AsyncIterable[StreamingAudioChunk]:
    async for audio in source:
        yield StreamingAudioChunk(audio=audio, is_final=False)
