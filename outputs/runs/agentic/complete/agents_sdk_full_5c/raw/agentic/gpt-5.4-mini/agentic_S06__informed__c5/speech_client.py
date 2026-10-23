from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Optional

from azure.cognitiveservices.speech import AudioConfig, SpeechConfig, SpeechSynthesisOutputFormat, SpeechSynthesizer

from speech_models import TextToSpeechRequest


@dataclass
class SpeechClientConfig:
    key: str
    region: str
    voice: Optional[str] = None
    output_format: str = "Audio16Khz32KBitRateMonoMp3"


class SpeechClientFactory:
    @staticmethod
    def from_env() -> SpeechClientConfig:
        return SpeechClientConfig(
            key=os.environ["AZURE_SPEECH_KEY"],
            region=os.environ["AZURE_SPEECH_REGION"],
            voice=os.getenv("AZURE_SPEECH_VOICE"),
        )

    @staticmethod
    def build_speech_config(cfg: SpeechClientConfig) -> SpeechConfig:
        speech_config = SpeechConfig(subscription=cfg.key, region=cfg.region)
        speech_config.set_speech_synthesis_output_format(
            getattr(SpeechSynthesisOutputFormat, cfg.output_format)
        )
        if cfg.voice:
            speech_config.speech_synthesis_voice_name = cfg.voice
        return speech_config

    @staticmethod
    def build_synthesizer(cfg: SpeechClientConfig, audio_filename: Optional[str] = None) -> SpeechSynthesizer:
        speech_config = SpeechClientFactory.build_speech_config(cfg)
        audio_config = AudioConfig(filename=audio_filename) if audio_filename else None
        return SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

    @staticmethod
    def request_to_voice(request: TextToSpeechRequest) -> Optional[str]:
        return request.voice or os.getenv("AZURE_SPEECH_VOICE")
