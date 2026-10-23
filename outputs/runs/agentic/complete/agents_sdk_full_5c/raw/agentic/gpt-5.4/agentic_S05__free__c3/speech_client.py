from __future__ import annotations

import os
from typing import Optional

import azure.cognitiveservices.speech as speechsdk

from speech_models import StreamingRecognitionConfig


DEFAULT_AZURE_SPEECH_REGION = os.getenv("AZURE_SPEECH_REGION", "eastus")
DEFAULT_AZURE_SPEECH_KEY = os.getenv("AZURE_SPEECH_KEY")
DEFAULT_AZURE_SPEECH_ENDPOINT = os.getenv("AZURE_SPEECH_ENDPOINT")


def create_speech_config(
    config: Optional[StreamingRecognitionConfig] = None,
    *,
    subscription_key: Optional[str] = None,
    region: Optional[str] = None,
    endpoint: Optional[str] = None,
) -> speechsdk.SpeechConfig:
    config = config or StreamingRecognitionConfig()
    key = subscription_key or DEFAULT_AZURE_SPEECH_KEY
    service_region = region or DEFAULT_AZURE_SPEECH_REGION
    custom_endpoint = endpoint or DEFAULT_AZURE_SPEECH_ENDPOINT

    if custom_endpoint:
        speech_config = speechsdk.SpeechConfig(endpoint=custom_endpoint, subscription=key)
    else:
        speech_config = speechsdk.SpeechConfig(subscription=key, region=service_region)

    speech_config.speech_recognition_language = config.language_code
    speech_config.set_property(
        speechsdk.PropertyId.SpeechServiceConnection_InitialSilenceTimeoutMs,
        "10000",
    )
    speech_config.set_property(
        speechsdk.PropertyId.SpeechServiceResponse_PostProcessingOption,
        "TrueText",
    )
    if config.enable_automatic_punctuation:
        speech_config.set_property(
            speechsdk.PropertyId.SpeechServiceResponse_RequestWordLevelTimestamps,
            "true",
        )
    return speech_config


def create_push_stream(*, sample_rate_hz: int = 16000, channels: int = 1) -> tuple[speechsdk.audio.PushAudioInputStream, speechsdk.audio.AudioConfig]:
    stream_format = speechsdk.audio.AudioStreamFormat(
        samples_per_second=sample_rate_hz,
        bits_per_sample=16,
        channels=channels,
    )
    push_stream = speechsdk.audio.PushAudioInputStream(stream_format=stream_format)
    audio_config = speechsdk.audio.AudioConfig(stream=push_stream)
    return push_stream, audio_config


def create_speech_recognizer(
    config: Optional[StreamingRecognitionConfig] = None,
    *,
    audio_config: Optional[speechsdk.audio.AudioConfig] = None,
) -> speechsdk.SpeechRecognizer:
    cfg = config or StreamingRecognitionConfig()
    speech_config = create_speech_config(cfg)
    if audio_config is None:
        audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
    return speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
