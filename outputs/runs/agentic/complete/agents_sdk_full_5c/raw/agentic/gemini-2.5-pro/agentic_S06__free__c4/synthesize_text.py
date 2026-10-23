"""
Uses Google Cloud Text-to-Speech to synthesize plain text to an audio byte stream.
"""
from google.cloud import texttospeech
from speech_client import get_google_tts_client

def synthesize_google_tts(text: str, voice_name: str = "en-US-Wavenet-D") -> bytes:
    """
    Synthesizes plain text into speech using Google Cloud TTS.

    Args:
        text: The text to synthesize.
        voice_name: The name of the Google Cloud TTS voice to use.

    Returns:
        The audio content as a byte stream (MP3).
    """
    client = get_google_tts_client()

    synthesis_input = texttospeech.SynthesisInput(text=text)

    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name=voice_name,
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL,
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    return response.audio_content
