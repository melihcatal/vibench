from __future__ import annotations

import os

import azure.cognitiveservices.speech as speechsdk

from model_models import NormalizedResponse


SPEECH_KEY = os.environ.get("AZURE_SPEECH_KEY", "")
SPEECH_REGION = os.environ.get("AZURE_SPEECH_REGION", "")
VOICE = os.environ.get("AZURE_SPEECH_VOICE", "en-US-JennyNeural")


def platform_brief_audio(output: str | NormalizedResponse, path: str = "briefing_audio.wav") -> str:
    text = output.text if isinstance(output, NormalizedResponse) else output
    speech_config = speechsdk.SpeechConfig(subscription=SPEECH_KEY, region=SPEECH_REGION)
    speech_config.speech_synthesis_voice_name = VOICE
    audio_config = speechsdk.audio.AudioOutputConfig(filename=path)
    synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
    synthesizer.speak_text_async(text).get()
    return path
