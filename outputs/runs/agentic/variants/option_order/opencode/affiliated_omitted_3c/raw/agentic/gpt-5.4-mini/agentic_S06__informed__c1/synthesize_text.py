from google.cloud import texttospeech

from speech_client import (
    build_client,
    default_audio_encoding,
    default_voice_language,
    default_voice_name,
)
from speech_models import SpeechRequest, SpeechResponse


def synthesize_text(text: str) -> bytes:
    client = build_client()
    request = SpeechRequest(
        text=text, locale=default_voice_language(), voice_name=default_voice_name()
    )
    payload = request.normalized()
    voice = texttospeech.VoiceSelectionParams(
        language_code=payload.get("locale", default_voice_language())
    )
    if payload.get("voice_name"):
        voice.name = payload["voice_name"]
    synthesis_input = texttospeech.SynthesisInput(text=payload["text"])
    audio_config = texttospeech.AudioConfig(audio_encoding=default_audio_encoding())
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )
    return SpeechResponse(audio_content=response.audio_content).audio_content
