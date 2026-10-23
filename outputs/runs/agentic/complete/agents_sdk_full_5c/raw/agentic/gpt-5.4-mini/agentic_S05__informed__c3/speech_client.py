from __future__ import annotations

import os
from dataclasses import dataclass
from typing import AsyncIterable, Iterable, Iterator, Optional

import azure.cognitiveservices.speech as speechsdk

from speech_models import SpeechChunk, StreamingTranscriptEvent, StreamingTranscriptResult


@dataclass
class SpeechConfig:
    key: str
    region: str
    language: str = "en-US"
    enable_punctuation: bool = True
    endpoint_id: Optional[str] = None


def load_speech_config() -> SpeechConfig:
    key = os.environ.get("AZURE_SPEECH_KEY", "")
    region = os.environ.get("AZURE_SPEECH_REGION", "")
    language = os.environ.get("AZURE_SPEECH_LANGUAGE", "en-US")
    enable_punctuation = os.environ.get("AZURE_SPEECH_ENABLE_PUNCTUATION", "true").lower() in {"1", "true", "yes", "on"}
    endpoint_id = os.environ.get("AZURE_SPEECH_ENDPOINT_ID")
    return SpeechConfig(key=key, region=region, language=language, enable_punctuation=enable_punctuation, endpoint_id=endpoint_id)


class AzureSpeechStreamingClient:
    def __init__(self, config: Optional[SpeechConfig] = None):
        self.config = config or load_speech_config()
        speech_config = speechsdk.SpeechConfig(subscription=self.config.key, region=self.config.region)
        speech_config.speech_recognition_language = self.config.language
        if self.config.enable_punctuation:
            speech_config.set_property(speechsdk.PropertyId.SpeechServiceResponse_RequestWordLevelTimestamps, "true")
        if self.config.endpoint_id:
            speech_config.endpoint_id = self.config.endpoint_id
        self._speech_config = speech_config

    def recognize_from_microphone(self) -> speechsdk.SpeechRecognizer:
        audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
        return speechsdk.SpeechRecognizer(speech_config=self._speech_config, audio_config=audio_config)

    def recognize_from_push_stream(self) -> tuple[speechsdk.SpeechRecognizer, speechsdk.audio.PushAudioInputStream]:
        stream_format = speechsdk.audio.AudioStreamFormat(samples_per_second=16000, bits_per_sample=16, channels=1)
        push_stream = speechsdk.audio.PushAudioInputStream(stream_format=stream_format)
        audio_config = speechsdk.audio.AudioConfig(stream=push_stream)
        recognizer = speechsdk.SpeechRecognizer(speech_config=self._speech_config, audio_config=audio_config)
        return recognizer, push_stream

    async def push_chunks(self, chunks: AsyncIterable[SpeechChunk], push_stream: speechsdk.audio.PushAudioInputStream) -> None:
        async for chunk in chunks:
            push_stream.write(chunk.audio)
        push_stream.close()


def event_to_transcript(event: object, is_final: bool) -> StreamingTranscriptEvent:
    text = getattr(event, "result", None)
    if text is not None:
        text = getattr(text, "text", "")
    else:
        text = getattr(event, "text", "")
    return StreamingTranscriptEvent(text=text or "", is_final=is_final, raw={"provider": "azure-cognitiveservices-speech"})


def collect_result(events: Iterable[StreamingTranscriptEvent]) -> StreamingTranscriptResult:
    return StreamingTranscriptResult(events=list(events))
