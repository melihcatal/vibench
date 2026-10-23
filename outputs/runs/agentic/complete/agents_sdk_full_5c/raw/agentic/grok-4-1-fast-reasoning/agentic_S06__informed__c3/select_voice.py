import os
from typing import List, Dict, Optional
import azure.cognitiveservices.speech as speechsdk
from speech_models import VoiceInfo, voice_to_info

def list_voices(locale: Optional[str] = None) -> List[VoiceInfo]:
    """
    List available voices for Azure AI Speech TTS, optionally filtered by locale.
    """
    key = os.getenv("AZURE_SPEECH_KEY")
    region = os.getenv("AZURE_SPEECH_REGION")
    voice_result = speechsdk.Voice.list_voices_async(key, region).get()
    voices: List[VoiceInfo] = []
    for voice in voice_result.voices:
        info = voice_to_info(voice)
        if locale is None or info["locale"].startswith(locale):
            voices.append(info)
    return voices

def select_voice(locale: str, gender: Optional[str] = "Female") -> str:
    """
    Select first matching voice for locale and optional gender.
    """
    voices = list_voices(locale)
    for info in voices:
        if gender is None or info["gender"].lower() == gender.lower():
            return info["name"]
    if voices:
        return voices[0]["name"]
    raise ValueError(f"No voices available for locale '{locale}'")
