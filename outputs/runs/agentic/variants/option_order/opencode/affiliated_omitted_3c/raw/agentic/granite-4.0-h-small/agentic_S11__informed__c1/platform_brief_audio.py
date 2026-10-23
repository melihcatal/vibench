import json
from model_client import ManagedModelClient
from google.cloud import texttospeech


def platform_brief_audio(provider_output: str, voice: str = "en-US-Wavenet-D") -> dict:
    """Convert the model's textual response into a short speech audio file using Cloud Text-to-Speech.

    Returns a dict with the base64‑encoded audio data and associated metadata.
    """
    tts_client = texttospeech.TextToSpeechClient()
    input_ssml = texttospeech.SynthesisInput(ssml=f"<speak>{provider_output}</speak>")
    voice_selection = texttospeech.VoiceSelectionParams(
        language_code="en-US", name=voice
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.LINEAR16
    )
    response = tts_client.synthesize_speech(
        input=input_ssml, voice=voice_selection, audio_config=audio_config
    )
    audio_bytes = response.audio_content
    return {
        "audio_base64": audio_bytes.decode("latin-1"),
        "metadata": {"voice": voice, "encoding": "LINEAR16"},
    }
