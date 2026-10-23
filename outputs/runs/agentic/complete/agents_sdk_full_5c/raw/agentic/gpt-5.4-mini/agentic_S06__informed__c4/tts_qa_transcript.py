from __future__ import annotations

from typing import Optional

import azure.cognitiveservices.speech as speechsdk


def transcribe_tts_sample(audio_path: str, language: str = "en-US", subscription_key: Optional[str] = None, region: Optional[str] = None) -> str:
    speech_config = speechsdk.SpeechConfig(subscription=subscription_key, region=region)
    speech_config.speech_recognition_language = language
    audio_config = speechsdk.AudioConfig(filename=audio_path)
    recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
    result = recognizer.recognize_once()
    return result.text
