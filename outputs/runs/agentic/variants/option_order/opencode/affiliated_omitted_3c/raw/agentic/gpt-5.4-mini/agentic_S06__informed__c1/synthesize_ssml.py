from google.cloud import texttospeech

from speech_client import (
    build_client,
    default_audio_encoding,
    default_voice_language,
    default_voice_name,
)
from speech_models import SpeechRequest, SpeechResponse


def synthesize_ssml(ssml: str, speaking_rate: float = 1.0, pitch: float = 0.0) -> bytes:
    client = build_client()
    request = SpeechRequest(
        text="",
        ssml=ssml,
        locale=default_voice_language(),
        voice_name=default_voice_name(),
        speaking_rate=speaking_rate,
        pitch=pitch,
    )
    payload = request.normalized()
    voice = texttospeech.VoiceSelectionParams(
        language_code=payload.get("locale", default_voice_language())
    )
    if payload.get("voice_name"):
        voice.name = payload["voice_name"]
    synthesis_input = texttospeech.SynthesisInput(ssml=payload["ssml"])
    audio_config = texttospeech.AudioConfig(
        audio_encoding=default_audio_encoding(),
        speaking_rate=speaking_rate,
        pitch=pitch,
    )
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )
    return SpeechResponse(audio_content=response.audio_content).audio_content
