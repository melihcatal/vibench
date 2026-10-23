from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache
from typing import Optional

import azure.cognitiveservices.speech as speechsdk

from speech_models import TTSRequest, TTSResponse


@dataclass(frozen=True)
class SpeechConfig:
    key: str
    region: str
    default_voice: Optional[str] = None
    output_format: str = "audio-24khz-48kbitrate-mono-mp3"


@lru_cache(maxsize=1)
def load_config() -> SpeechConfig:
    key = os.getenv("AZURE_SPEECH_KEY", "")
    region = os.getenv("AZURE_SPEECH_REGION", "")
    default_voice = os.getenv("AZURE_SPEECH_VOICE")
    if not key or not region:
        raise RuntimeError("AZURE_SPEECH_KEY and AZURE_SPEECH_REGION are required")
    return SpeechConfig(key=key, region=region, default_voice=default_voice)


def create_speech_synthesizer(voice_name: Optional[str] = None):
    cfg = load_config()
    speech_config = speechsdk.SpeechConfig(subscription=cfg.key, region=cfg.region)
    speech_config.set_speech_synthesis_output_format(
        speechsdk.SpeechSynthesisOutputFormat[cfg.output_format]
    )
    if voice_name or cfg.default_voice:
        speech_config.speech_synthesis_voice_name = voice_name or cfg.default_voice
    audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=False)
    return speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)


def synthesize_text_request(request: TTSRequest) -> TTSResponse:
    synth = create_speech_synthesizer(request.voice_name)
    if request.ssml:
        result = synth.speak_ssml_async(request.text).get()
    else:
        result = synth.speak_text_async(request.text).get()
    if result.reason != speechsdk.ResultReason.SynthesizingAudioCompleted:
        raise RuntimeError(f"Speech synthesis failed: {result.reason}")
    return TTSResponse(audio=result.audio_data, metadata={"reason": str(result.reason)})
