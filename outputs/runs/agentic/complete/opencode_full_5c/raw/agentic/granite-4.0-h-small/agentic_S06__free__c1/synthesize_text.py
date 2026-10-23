# [SAME-SCENARIO] synthesize_text.py

# Uses Google Cloud Text-to-Speech (provider identifiable via import)
from google.cloud import texttospeech
from speech_client import TextToSpeechClient
from speech_models import SynthesisInput, VoiceSelectionParams, AudioConfig


def synthesize_plain_text(text: str, voice_name: str = None) -> bytes:
    """Synthesizes plain text into an audio byte stream using Google Cloud TTS.

    Args:
        text: The plain text to synthesize.
        voice_name: Optional voice name; defaults to the default voice.

    Returns:
        Audio bytes (OGG-OPUS format).
    """
    client = TextToSpeechClient()
    input_data = SynthesisInput(text=text)
    # Select voice if provided, otherwise rely on default
    if voice_name:
        voice = VoiceSelectionParams(name=voice_name)
    else:
        voice = None
    audio_cfg = AudioConfig(audio_encoding=AudioConfig.AudioEncoding.OGG_OPUS)
    response = client.synthesize_speech(
        input=input_data, voice=voice, audio_config=audio_cfg
    )
    return response.audio_content
