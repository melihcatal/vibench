from google.cloud import texttospeech
from speech_client import get_tts_client

def synthesize_ssml(ssml_text: str) -> bytes:
    """
    Synthesizes speech from SSML text.

    Args:
        ssml_text: The SSML text to synthesize.

    Returns:
        The synthesized audio content as bytes.
    """
    client = get_tts_client()

    synthesis_input = texttospeech.SynthesisInput(ssml=ssml_text)

    # Voice and language are often specified within the SSML
    # but we can provide a default if needed.
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    return response.audio_content
