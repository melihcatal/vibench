from google.cloud import texttospeech
from speech_client import get_tts_client

def synthesize_ssml_text(ssml: str, voice_name: str = "en-US-Wavenet-D") -> bytes:
    """
    Synthesizes speech from SSML text using Google Cloud Text-to-Speech.

    Args:
        ssml: The SSML text to synthesize.
        voice_name: The name of the voice to use (e.g., "en-US-Wavenet-D").

    Returns:
        The synthesized audio content as bytes.
    """
    client = get_tts_client()

    synthesis_input = texttospeech.SynthesisInput(ssml=ssml)

    language_code = "-".join(voice_name.split("-")[:2])
    voice = texttospeech.VoiceSelectionParams(
        language_code=language_code,
        name=voice_name,
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    return response.audio_content
