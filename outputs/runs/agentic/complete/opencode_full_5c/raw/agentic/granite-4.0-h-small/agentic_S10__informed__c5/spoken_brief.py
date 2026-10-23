import os
from google.cloud import texttospeech
from model_models import LLMResponse


def generate_spoken_brief(text: str, voice_name: str = "en-US-Wavenet-D") -> bytes:
    """Converts model output to spoken audio using Google Cloud Text-to-Speech.

    Returns audio data as bytes (OGG format).
    """
    client = texttospeech.TextToSpeechClient()
    input_text = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(language_code="en-US", name=voice_name)
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.OGG_OPUS
    )
    response = client.synthesize_speech(
        input=input_text, voice=voice, audio_config=audio_config
    )
    return response.audio_content
