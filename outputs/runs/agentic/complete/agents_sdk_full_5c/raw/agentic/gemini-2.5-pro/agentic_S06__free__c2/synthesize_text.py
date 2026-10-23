from google.cloud import texttospeech_v1 as texttospeech

from speech_client import get_tts_client


def synthesize_plain_text(
    text: str, voice_name: str = "en-US-Standard-C"
) -> bytes:
    """
    Synthesizes plain text into speech.

    Args:
        text: The text to synthesize.
        voice_name: The name of the voice to use.

    Returns:
        The synthesized audio content as bytes.
    """
    client = get_tts_client()

    synthesis_input = texttospeech.SynthesisInput(text=text)

    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US", name=voice_name
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    return response.audio_content
