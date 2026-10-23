import os
from typing import Any, Dict
from google.cloud import texttospeech_v1 as texttospeech

def generate_briefing_audio(provider: str, raw_response: Any, locale: str = "en-US") -> bytes:
    """Convert platform output into a short spoken briefing.
    Uses Google Cloud Text-to-Speech API to synthesize audio.
    Returns raw audio bytes (OGG_OPUS format)."
    if provider != "Hugging Face":
        raise NotImplementedError(f"TTS not implemented for provider {provider}")
    if not os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
        raise EnvironmentError("Set GOOGLE_APPLICATION_CREDENTIALS to point at your Google Cloud credentials JSON")
    client = texttospeech.TextToSpeechClient()
    synthesis_input = texttospeech.SynthesisInput(text=raw_response.get("output", ""))
    voice = texttospeech.VoiceSelectionParams(language_code=locale, ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL)
    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.OGG_OPUS)
    response = client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)
    return response.audio_content