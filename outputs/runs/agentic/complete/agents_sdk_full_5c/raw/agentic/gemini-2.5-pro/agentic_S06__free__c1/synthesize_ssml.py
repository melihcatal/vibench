from google.cloud import texttospeech
from speech_client import get_tts_client
from speech_models import VoiceSelectionParams

def synthesize_ssml_to_audio(ssml_text: str, voice_params: VoiceSelectionParams) -> bytes:
    """
    Synthesizes SSML text into audio bytes using Google Cloud Text-to-Speech.

    Args:
        ssml_text: The SSML text to synthesize.
        voice_params: The voice selection parameters.

    Returns:
        The synthesized audio content as bytes.
    """
    client = get_tts_client()

    synthesis_input = texttospeech.SynthesisInput(ssml=ssml_text)

    voice = texttospeech.VoiceSelectionParams(
        language_code=voice_params.language_code,
        name=voice_params.name
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.LINEAR16
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    return response.audio_content
