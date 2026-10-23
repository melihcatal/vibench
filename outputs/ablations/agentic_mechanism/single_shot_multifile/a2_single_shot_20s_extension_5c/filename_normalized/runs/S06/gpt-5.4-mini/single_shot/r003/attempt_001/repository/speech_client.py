from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache
from typing import List, Optional

import azure.cognitiveservices.speech as speechsdk

from speech_models import SynthesisRequest, SynthesisResponse, VoiceInfo


@dataclass(frozen=True)
class AzureSpeechConfig:
    subscription_key: str
    region: str
    default_voice: str


@lru_cache(maxsize=1)
def get_config() -> AzureSpeechConfig:
    subscription_key = os.environ.get("AZURE_SPEECH_KEY") or os.environ.get("AZURE_SPEECH_SUBSCRIPTION_KEY")
    region = os.environ.get("AZURE_SPEECH_REGION", "eastus")
    default_voice = os.environ.get("AZURE_SPEECH_VOICE", "en-US-JennyNeural")
    if not subscription_key:
        raise ValueError("AZURE_SPEECH_KEY or AZURE_SPEECH_SUBSCRIPTION_KEY is required")
    return AzureSpeechConfig(subscription_key=subscription_key, region=region, default_voice=default_voice)


def get_tts_client() -> "AzureSpeechClient":
    return AzureSpeechClient(get_config())


def voice_name_for_locale(locale: str) -> str:
    return {
        "en-us": "en-US-JennyNeural",
        "en-gb": "en-GB-LibbyNeural",
        "es-es": "es-ES-ElviraNeural",
        "fr-fr": "fr-FR-DeniseNeural",
    }.get(locale.lower(), get_config().default_voice)


@dataclass
class AzureSpeechClient:
    config: AzureSpeechConfig

    def _speech_config(self) -> speechsdk.SpeechConfig:
        speech_config = speechsdk.SpeechConfig(subscription=self.config.subscription_key, region=self.config.region)
        speech_config.set_speech_synthesis_output_format(speechsdk.SpeechSynthesisOutputFormat.Audio16Khz32KBitRateMonoMp3)
        return speech_config

    def synthesize(self, request: SynthesisRequest) -> SynthesisResponse:
        speech_config = self._speech_config()
        speech_config.speech_synthesis_voice_name = request.voice or self.config.default_voice
        audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=False)
        synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
        if request.is_ssml:
            result = synthesizer.speak_ssml_async(request.text).get()
        else:
            result = synthesizer.speak_text_async(request.text).get()
        if result.reason != speechsdk.ResultReason.SynthesizingAudioCompleted:
            details = speechsdk.SpeechSynthesisCancellationDetails.from_result(result)
            raise RuntimeError(f"Azure Speech synthesis failed: {details.reason} {details.error_details}")
        audio_bytes = result.audio_data or b""
        return SynthesisResponse(audio_bytes=audio_bytes, content_type="audio/mpeg", voice=request.voice or self.config.default_voice)

    def list_voices(self) -> List[VoiceInfo]:
        speech_config = self._speech_config()
        synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=None)
        result = synthesizer.get_voices_async().get()
        voices: List[VoiceInfo] = []
        for v in result.voices:
            locales = list(v.locales)
            voices.append(VoiceInfo(name=v.name, locale=locales[0] if locales else "", locales=locales, gender=getattr(v, "gender", None)))
        return voices


def resolve_voice(name: Optional[str], locale: str) -> VoiceInfo:
    selected = name or voice_name_for_locale(locale)
    return VoiceInfo(name=selected, locale=locale, locales=[locale], gender=None)
