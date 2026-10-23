from __future__ import annotations

import os
from functools import lru_cache
from typing import List, Optional

import azure.cognitiveservices.speech as speechsdk

from speech_models import TextToSpeechRequest, TextToSpeechResponse, VoiceChoice


@lru_cache(maxsize=1)
def _speech_config() -> speechsdk.SpeechConfig:
    key = os.environ.get("AZURE_SPEECH_KEY")
    region = os.environ.get("AZURE_SPEECH_REGION")
    if not key or not region:
        raise RuntimeError("AZURE_SPEECH_KEY and AZURE_SPEECH_REGION are required for Azure AI Speech TTS")
    config = speechsdk.SpeechConfig(subscription=key, region=region)
    return config


def audio_output_config_for_path(path: str) -> speechsdk.audio.AudioOutputConfig:
    return speechsdk.audio.AudioOutputConfig(filename=path)


def speech_synthesizer(output: Optional[speechsdk.audio.AudioOutputConfig] = None) -> speechsdk.SpeechSynthesizer:
    return speechsdk.SpeechSynthesizer(speech_config=_speech_config(), audio_config=output)


def available_voices(locale: Optional[str] = None) -> List[VoiceChoice]:
    synthesizer = speech_synthesizer()
    result = synthesizer.get_voices_async(locale or "").get()
    voices: List[VoiceChoice] = []
    for voice in result.voices:
        voices.append(
            VoiceChoice(
                name=voice.short_name,
                locale=voice.locale,
                gender=str(voice.gender),
                description=getattr(voice, "display_name", None),
            )
        )
    return voices


def synthesize_request(request: TextToSpeechRequest) -> TextToSpeechResponse:
    synthesizer = speech_synthesizer()
    if request.voice:
        synthesizer.speech_config.speech_synthesis_voice_name = request.voice
    if request.ssml:
        result = synthesizer.speak_ssml_async(request.text).get()
    else:
        result = synthesizer.speak_text_async(request.text).get()
    if result.reason != speechsdk.ResultReason.SynthesizingAudioCompleted:
        raise RuntimeError(f"Azure synthesis failed: {result.reason}")
    audio = bytes(result.audio_data)
    return TextToSpeechResponse(audio_bytes=audio, content_type="audio/mpeg", voice=request.voice, locale=request.locale)
