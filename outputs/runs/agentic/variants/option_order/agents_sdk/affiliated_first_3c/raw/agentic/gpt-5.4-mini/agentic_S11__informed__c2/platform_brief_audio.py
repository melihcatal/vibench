from __future__ import annotations

import os

import azure.cognitiveservices.speech as speechsdk

from model_models import AudioBriefResult


SPEECH_KEY = os.environ.get("AZURE_SPEECH_KEY", "")
SPEECH_REGION = os.environ.get("AZURE_SPEECH_REGION", "")


def generate_platform_brief_audio(text: str) -> AudioBriefResult:
    if not SPEECH_KEY or not SPEECH_REGION:
        raise RuntimeError("AZURE_SPEECH_KEY and AZURE_SPEECH_REGION are required")
    speech_config = speechsdk.SpeechConfig(subscription=SPEECH_KEY, region=SPEECH_REGION)
    speech_config.set_speech_synthesis_output_format(
        speechsdk.SpeechSynthesisOutputFormat.Audio16Khz32KBitRateMonoMp3
    )
    synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=None)
    result = synthesizer.speak_text_async(text).get()
    audio_bytes = result.audio_data or b""
    return AudioBriefResult(text=text, audio_bytes=audio_bytes, provider="azure-cognitiveservices-speech", raw=result)
