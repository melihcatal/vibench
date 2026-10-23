# [LATER-STEP] platform_brief_audio.py
# Generate spoken briefings from platform outputs (TTS)

from google.cloud import texttospeech
from model_models import ProviderResponse


def create_audio_brief(text: str, voice_name: str = "en-US-Wavenet-D") -> bytes:
    """Convert the given text to spoken audio (MP3) using Google Cloud Text-to-Speech."""
    client = texttospeech.TextToSpeechClient()
    input_ssml = texttospeech.SynthesisInput(ssml=f"<speak>{text}</speak>")
    voice = texttospeech.VoiceSelectionParams(language_code="en-US", name=voice_name)
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )
    response = client.synthesize_speech(
        input=input_ssml, voice=voice, audio_config=audio_config
    )
    # Return raw MP3 bytes
    return response.audio_content
