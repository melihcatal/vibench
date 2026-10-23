from google.cloud import texttospeech
from speech_client import get_tts_client


def synthesize_ssml(ssml_text: str) -> bytes:
    """
    Synthesizes SSML text into speech audio bytes.

    Args:
        ssml_text: The SSML text to synthesize.

    Returns:
        The synthesized audio content in bytes.
    """
    client = get_tts_client()

    synthesis_input = texttospeech.SynthesisInput(ssml=ssml_text)

    # Note: Voice and language are often specified within the SSML itself.
    # If not, a default voice can be configured here.
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US", name="en-US-Standard-A"
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    return response.audio_content
