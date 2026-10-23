from __future__ import annotations

from typing import Any, Dict

import azure.cognitiveservices.speech as speechsdk


def transcribe_tts_audio(audio_path: str, language: str = "en-US") -> Dict[str, Any]:
    speech_config = speechsdk.SpeechConfig(subscription=None, region=None)
    speech_config.speech_recognition_language = language
    audio_config = speechsdk.AudioConfig(filename=audio_path)
    recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
    result = recognizer.recognize_once_async().get()
    return {"text": result.text, "reason": str(result.reason)}
