import os
from google.cloud import texttospeech

def get_text_to_speech_client():
    """Provides a configured Google Cloud Text-to-Speech client."""
    return texttospeech.TextToSpeechClient()

def get_default_voice_params(language_code: str = "en-US") -> texttospeech.VoiceSelectionParams:
    """Returns default voice selection parameters for a given language code."""
    return texttospeech.VoiceSelectionParams(
        language_code=language_code,
        name=f"{language_code}-Wavenet-A", # Defaulting to a common Wavenet voice
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL,
    )

def get_default_audio_config(output_format: str = "MP3") -> texttospeech.AudioConfig:
    """Returns default audio configuration parameters."""
    return texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding[output_format],
    )
