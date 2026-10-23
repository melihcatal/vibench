from google.cloud import texttospeech

from speech_client import get_speech_client
from speech_models import SpeechRequest


def synthesize_ssml(request: SpeechRequest) -> bytes:
    """Synthesizes SSML text into audio bytes."""
    client = get_speech_client()

    synthesis_input = texttospeech.SynthesisInput(ssml=request.text)

    voice = texttospeech.VoiceSelectionParams(
        language_code=request.language_code,
        name=request.voice_name
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.LINEAR16
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    return response.audio_content
