from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache
from typing import List, Optional

import azure.cognitiveservices.speech as speechsdk

from speech_models import TTSRequest, VoiceSelection, build_ssml, normalize_locale


@dataclass(frozen=True)
class SpeechConfig:
    key: str
    region: str
    default_voice: str = "en-US-JennyNeural"
    default_locale: str = "en-US"


@lru_cache(maxsize=1)
def load_config() -> SpeechConfig:
    key = os.getenv("AZURE_SPEECH_KEY", "")
    region = os.getenv("AZURE_SPEECH_REGION", "")
    default_voice = os.getenv("AZURE_SPEECH_VOICE", "en-US-JennyNeural")
    default_locale = os.getenv("AZURE_SPEECH_LOCALE", "en-US")
    if not key or not region:
        raise RuntimeError("AZURE_SPEECH_KEY and AZURE_SPEECH_REGION are required")
    return SpeechConfig(key=key, region=region, default_voice=default_voice, default_locale=default_locale)


def create_speech_config() -> speechsdk.SpeechConfig:
    cfg = load_config()
    speech_config = speechsdk.SpeechConfig(subscription=cfg.key, region=cfg.region)
    speech_config.speech_synthesis_voice_name = cfg.default_voice
    return speech_config


def create_synthesizer() -> speechsdk.SpeechSynthesizer:
    speech_config = create_speech_config()
    audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=False)
    return speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)


def available_voices(locale: Optional[str] = None) -> List[VoiceSelection]:
    cfg = load_config()
    speech_config = create_speech_config()
    synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=None)
    result = synthesizer.get_voices_async(normalize_locale(locale) or cfg.default_locale).get()
    voices: List[VoiceSelection] = []
    for voice in result.voices:
        voices.append(VoiceSelection(name=voice.name, locale=voice.locale, gender=getattr(voice, "gender", None), provider="azure"))
    return voices


def synthesize_text(request: TTSRequest) -> bytes:
    synthesizer = create_synthesizer()
    if request.ssml:
        ssml = build_ssml(request.normalized_text(), request.normalized_voice() or load_config().default_voice, request.prosody_rate, request.prosody_pitch, request.locale)
        result = synthesizer.speak_ssml_async(ssml).get()
    else:
        text = request.normalized_text()
        if request.voice:
            synthesizer.speech_config.speech_synthesis_voice_name = request.voice
        result = synthesizer.speak_text_async(text).get()
    if result.reason != speechsdk.ResultReason.SynthesizingAudioCompleted:
        raise RuntimeError(f"Azure Speech synthesis failed: {result.reason}")
    return bytes(result.audio_data)
