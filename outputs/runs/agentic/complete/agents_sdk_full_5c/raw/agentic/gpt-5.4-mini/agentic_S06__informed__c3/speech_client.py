from __future__ import annotations

import os
from dataclasses import dataclass
from typing import List, Optional

import azure.cognitiveservices.speech as speechsdk

from speech_models import TextToSpeechRequest, TextToSpeechResponse, VoiceOption, build_ssml, normalize_locale


@dataclass(frozen=True)
class SpeechConfig:
    key: str
    region: str
    output_format: str = "audio-24khz-48kbitrate-mono-mp3"


def load_speech_config() -> SpeechConfig:
    key = os.environ.get("AZURE_SPEECH_KEY", "")
    region = os.environ.get("AZURE_SPEECH_REGION", "")
    if not key or not region:
        raise EnvironmentError("AZURE_SPEECH_KEY and AZURE_SPEECH_REGION are required")
    return SpeechConfig(key=key, region=region)


def build_speech_synthesizer(config: Optional[SpeechConfig] = None) -> speechsdk.SpeechSynthesizer:
    cfg = config or load_speech_config()
    speech_config = speechsdk.SpeechConfig(subscription=cfg.key, region=cfg.region)
    speech_config.set_speech_synthesis_output_format(getattr(speechsdk.SpeechSynthesisOutputFormat, cfg.output_format))
    return speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=None)


def synthesize_with_azure(request: TextToSpeechRequest, config: Optional[SpeechConfig] = None) -> TextToSpeechResponse:
    synthesizer = build_speech_synthesizer(config)
    if request.ssml:
        ssml = build_ssml(request.normalized_text(), request.normalized_voice() or "en-US-AriaNeural", normalize_locale(request.locale), request.pitch, request.rate, request.volume)
        result = synthesizer.speak_ssml_async(ssml).get()
    else:
        result = synthesizer.speak_text_async(request.normalized_text()).get()
    if result.reason != speechsdk.ResultReason.SynthesizingAudioCompleted:
        raise RuntimeError(f"Azure Speech synthesis failed: {result.reason}")
    return TextToSpeechResponse(audio_bytes=result.audio_data, content_type="audio/mpeg", voice=request.voice, locale=request.locale)


def list_azure_voices(locale: Optional[str] = None, config: Optional[SpeechConfig] = None) -> List[VoiceOption]:
    synthesizer = build_speech_synthesizer(config)
    locale = normalize_locale(locale)
    voices = synthesizer.get_voices_async(locale).get()
    if voices.reason != speechsdk.ResultReason.VoicesListRetrieved:
        raise RuntimeError("Azure voice list retrieval failed")
    result: List[VoiceOption] = []
    for voice in voices.voices:
        result.append(VoiceOption(name=voice.short_name, locale=voice.locale, gender=getattr(voice, "gender", None), sample_rate_hz=None, metadata={"local_name": voice.local_name}))
    return result
