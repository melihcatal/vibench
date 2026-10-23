from google.cloud import texttospeech
from speech_client import get_speech_client

def synthesize_ssml_to_audio(ssml: str) -> bytes:
    """
    Synthesizes SSML into audio bytes using Google Cloud Text-to-Speech.

    Args:
        ssml: The SSML string to synthesize.

    Returns:
        The synthesized audio content in bytes.
    """
    client = get_speech_client()

    synthesis_input = texttospeech.SynthesisInput(ssml=ssml)

    # Voice selection is embedded within the SSML, but we must still
    # provide a default voice parameter object, though its fields are optional.
    voice = texttospeech.VoiceSelectionParams()

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    return response.audio_content
