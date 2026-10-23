import os
from typing import Optional

from google.cloud import texttospeech

from speech_models import SpeechRequest, normalize_locale


def get_client() -> texttospeech.TextToSpeechClient:
    return texttospeech.TextToSpeechClient()


def get_voice_name(locale: Optional[str] = None, voice: Optional[str] = None) -> Optional[str]:
    if voice:
        return voice
    if locale:
        locale = normalize_locale(locale)
        if locale == "en-US":
            return "en-US-Neural2-F"
        if locale == "en-GB":
            return "en-GB-Neural2-C"
    return os.getenv("GOOGLE_TTS_VOICE")


def build_synthesis_input(request: SpeechRequest):
    if request.ssml:
        return texttospeech.SynthesisInput(ssml=request.text)
    return texttospeech.SynthesisInput(text=request.text)
