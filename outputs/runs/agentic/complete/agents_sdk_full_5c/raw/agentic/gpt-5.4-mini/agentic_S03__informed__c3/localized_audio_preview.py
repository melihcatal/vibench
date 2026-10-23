from __future__ import annotations

import os

import azure.cognitiveservices.speech as speechsdk

from translation_models import AudioPreviewResult


AZURE_TTS_VOICE = "en-US-JennyNeural"


def generate_spoken_preview(text: str, language: str) -> AudioPreviewResult:
    speech_config = speechsdk.SpeechConfig(
        subscription=os.environ["AZURE_SPEECH_KEY"],
        region=os.environ["AZURE_SPEECH_REGION"],
    )
    speech_config.speech_synthesis_voice_name = AZURE_TTS_VOICE
    audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=False)
    synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
    result = synthesizer.speak_text_async(text).get()
    audio_bytes = result.audio_data or b""
    return AudioPreviewResult(provider="Azure AI Speech TTS", audio_content=audio_bytes, audio_format="audio/wav", metadata={"voice": AZURE_TTS_VOICE, "language": language})
