from google.cloud import texttospeech

from speech_client import get_speech_client
from speech_models import SpeechSynthesisRequest


def synthesize_ssml(req: SpeechSynthesisRequest) -> bytes:
    """Synthesizes speech from the input SSML."""
    if not req.ssml:
        raise ValueError("SSML text must be provided for SSML synthesis.")

    client = get_speech_client()

    synthesis_input = texttospeech.SynthesisInput(ssml=req.ssml)

    voice = texttospeech.VoiceSelectionParams(
        language_code=req.language_code, name=req.voice_name
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.LINEAR16
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    return response.audio_content
