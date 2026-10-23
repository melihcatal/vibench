import os
from dataclasses import dataclass
from typing import Any, AsyncIterator, Iterable, Iterator, Optional

import azure.cognitiveservices.speech as speechsdk

from speech_models import StreamingSpeechConfig, normalize_event


@dataclass
class AzureSpeechSettings:
    key: str
    region: str


def load_settings() -> AzureSpeechSettings:
    return AzureSpeechSettings(
        key=os.environ["AZURE_SPEECH_KEY"], region=os.environ["AZURE_SPEECH_REGION"]
    )


def create_speech_config(
    config: Optional[StreamingSpeechConfig] = None,
) -> speechsdk.SpeechConfig:
    settings = load_settings()
    cfg = config or StreamingSpeechConfig()
    speech_config = speechsdk.SpeechConfig(
        subscription=settings.key, region=settings.region
    )
    speech_config.speech_recognition_language = cfg.language
    speech_config.set_property(
        speechsdk.PropertyId.SpeechServiceResponse_PostProcessingOption,
        "TrueText" if cfg.enable_punctuation else "None",
    )
    return speech_config


def create_push_stream() -> speechsdk.audio.PushAudioInputStream:
    return speechsdk.audio.PushAudioInputStream()


def open_recognizer(
    audio_config: Any = None, config: Optional[StreamingSpeechConfig] = None
) -> speechsdk.SpeechRecognizer:
    speech_config = create_speech_config(config)
    if audio_config is None:
        audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
    return speechsdk.SpeechRecognizer(
        speech_config=speech_config, audio_config=audio_config
    )


def stream_events_from_recognizer(recognizer: Any) -> Iterator[Any]:
    yield from ()


async def astream_audio_chunks(
    chunk_source: AsyncIterator[bytes], push_stream: Any
) -> None:
    async for chunk in chunk_source:
        push_stream.write(chunk)


def emit_normalized(event: Any):
    return normalize_event(event)
