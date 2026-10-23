from google.cloud import texttospeech

from speech_client import get_speech_client
from speech_models import SpeechRequest


def synthesize_ssml(req: SpeechRequest) -> bytes:
    """
    Synthesizes speech from SSML.

    Args:
        req: A SpeechRequest object containing the SSML and voice settings.

    Returns:
        The synthesized audio content as bytes.
    """
    client = get_speech_client()

    synthesis_input = texttospeech.SynthesisInput(ssml=req.ssml)

    voice = texttospeech.VoiceSelectionParams(
        language_code=req.language_code,
        name=req.voice_name,
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL,
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    return response.audio_content
