import os
from dataclasses import dataclass
from functools import lru_cache
from typing import Optional

from azure.cognitiveservices import speech as speechsdk


@dataclass(frozen=True)
class SpeechConfig:
    subscription_key: str
    region: str
    output_format: str = "riff-16khz-16bit-mono-pcm"
    voice: Optional[str] = None


@lru_cache(maxsize=1)
def load_speech_config() -> SpeechConfig:
    key = os.getenv("AZURE_SPEECH_KEY", "")
    region = os.getenv("AZURE_SPEECH_REGION", "")
    voice = os.getenv("AZURE_SPEECH_VOICE")
    return SpeechConfig(subscription_key=key, region=region, voice=voice)


def create_speech_config(config: Optional[SpeechConfig] = None) -> speechsdk.SpeechConfig:
    cfg = config or load_speech_config()
    speech_config = speechsdk.SpeechConfig(subscription=cfg.subscription_key, region=cfg.region)
    speech_config.set_speech_synthesis_output_format(getattr(speechsdk.SpeechSynthesisOutputFormat, cfg.output_format))
    return speech_config


def create_synthesizer(audio_config=None, config: Optional[SpeechConfig] = None) -> speechsdk.SpeechSynthesizer:
    speech_config = create_speech_config(config)
    return speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)


def normalize_voice_name(locale: str, voice_name: Optional[str]) -> Optional[str]:
    if voice_name:
        return voice_name
    mapping = {
        "en-US": "en-US-JennyNeural",
        "en-GB": "en-GB-SoniaNeural",
        "es-ES": "es-ES-ElviraNeural",
        "fr-FR": "fr-FR-DeniseNeural",
        "de-DE": "de-DE-KatjaNeural",
    }
    return mapping.get(locale)
