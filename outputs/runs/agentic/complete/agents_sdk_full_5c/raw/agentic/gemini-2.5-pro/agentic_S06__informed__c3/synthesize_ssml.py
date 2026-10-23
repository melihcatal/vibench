from google.cloud import texttospeech
from speech_client import get_tts_client

def synthesize_ssml_text(ssml: str, voice_name: str = "en-US-Studio-O") -> bytes:
    """Synthesizes speech from the input SSML string."""
    client = get_tts_client()

    synthesis_input = texttospeech.SynthesisInput(ssml=ssml)

    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name=voice_name,
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    return response.audio_content
