import os
from google.cloud import texttospeech
from ibm_watson import TextToSpeechV1


def generate_spoken_preview(
    text: str, language_code: str = "es-ES", voice_name: str = "es-ES_Standard_A"
) -> bytes:
    """
    Generates a spoken audio preview of translated copy using multiple TTS providers.

    Args:
        text: The translated text to convert to speech.
        language_code: BCP-47 language tag for the TTS engine.
        voice_name: Specific voice identifier (optional).

    Returns:
        Audio content as bytes (WAV/MP3 depending on provider).
    """
    # GOOGLE Cloud Text-to-Speech (default)
    gclient = texttospeech.TextToSpeechClient()
    g_input = texttospeech.SynthesisInput(text=text)
    g_config = texttospeech.VoiceSelectionParams(
        language_code=language_code, name=voice_name
    )
    g_config.audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.LINEAR16
    )
    g_response = gclient.synthesize_speech(
        input=g_input, voice=g_config, audio_config=g_config.audio_config
    )
    # Return raw audio bytes
    return g_response.audio_content
