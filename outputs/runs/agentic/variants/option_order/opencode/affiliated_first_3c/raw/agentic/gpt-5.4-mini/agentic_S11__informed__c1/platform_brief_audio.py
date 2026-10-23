from __future__ import annotations

import os
import azure.cognitiveservices.speech as speechsdk


def platform_brief_audio(text: str) -> bytes:
    speech_key = os.environ.get("AZURE_SPEECH_KEY", "")
    speech_region = os.environ.get("AZURE_SPEECH_REGION", "")
    speech_config = speechsdk.SpeechConfig(
        subscription=speech_key, region=speech_region
    )
    audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=False)
    synthesizer = speechsdk.SpeechSynthesizer(
        speech_config=speech_config, audio_config=audio_config
    )
    result = synthesizer.speak_text_async(text).get()
    return result.audio_data
