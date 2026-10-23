from google.cloud import texttospeech
from speech_client import get_tts_client

def synthesize_plain_text(text: str, voice_name: str = "en-US-Standard-C") -> bytes:
    """
    Synthesizes speech from plain text using Google Cloud Text-to-Speech.

    Args:
        text: The text to synthesize.
        voice_name: The name of the voice to use (e.g., "en-US-Standard-C").

    Returns:
        The synthesized audio content as bytes.
    """
    client = get_tts_client()

    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Note: language_code is inferred from the voice name format (e.g., en-US)
    language_code = "-".join(voice_name.split("-")[:2])
    voice = texttospeech.VoiceSelectionParams(
        language_code=language_code,
        name=voice_name
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    return response.audio_content
