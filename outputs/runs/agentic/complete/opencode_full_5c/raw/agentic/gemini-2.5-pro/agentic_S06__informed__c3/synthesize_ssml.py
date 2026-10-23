from speech_client import get_speech_client
from google.cloud import texttospeech


def synthesize_ssml(ssml: str) -> bytes:
    """Synthesizes speech from the input SSML string."""
    client = get_speech_client()

    synthesis_input = texttospeech.SynthesisInput(ssml=ssml)

    # Voice selection is embedded in the SSML, but we must specify a voice here,
    # although it can be a generic one if the SSML specifies the voice.
    # For simplicity, we'll use a default voice, but the SSML will override it.
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name="en-US-Standard-C",
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    return response.audio_content
