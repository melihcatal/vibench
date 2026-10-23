import os
from google.cloud import texttospeech
from speech_client import get_tts_client
from speech_models import SynthesizeTextRequest


def synthesize_plain_text(request: SynthesizeTextRequest) -> bytes:
    """
    Synthesizes plain text to an audio byte stream using Google Cloud Text-to-Speech.
    Requires GOOGLE_APPLICATION_CREDENTIALS to be set.
    """
    client = get_tts_client()

    synthesis_input = texttospeech.SynthesisInput(text=request.text)
    voice = texttospeech.VoiceSelectionParams(
        language_code=request.language_code, name=request.voice_name
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding[request.audio_encoding]
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    return response.audio_content
