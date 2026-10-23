from google.cloud import texttospeech
from speech_client import get_tts_client


def synthesize_text(text: str, voice_name: str, language_code: str) -> bytes:
    """
    Synthesizes plain text into speech audio bytes.

    Args:
        text: The plain text to synthesize.
        voice_name: The name of the voice to use (e.g., 'en-US-Standard-C').
        language_code: The language code of the voice (e.g., 'en-US').

    Returns:
        The synthesized audio content in bytes.
    """
    client = get_tts_client()

    synthesis_input = texttospeech.SynthesisInput(text=text)

    voice = texttospeech.VoiceSelectionParams(
        language_code=language_code, name=voice_name
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    return response.audio_content
