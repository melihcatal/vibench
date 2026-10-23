from __future__ import annotations

from google.cloud import texttospeech

from speech_client import get_google_tts_client, resolve_audio_encoding
from speech_models import AudioArtifact, SynthesisRequest


GOOGLE_TTS_PROVIDER = "texttospeech.googleapis.com"


def synthesize_text(
    text: str,
    language_code: str = "en-US",
    voice_name: str | None = None,
    audio_encoding: str = "MP3",
) -> AudioArtifact:
    client = get_google_tts_client()
    request = SynthesisRequest(
        text=text,
        voice=voice_name,
        language_code=language_code,
        audio_encoding=audio_encoding,
    )
    synthesis_input = texttospeech.SynthesisInput(text=request.text)
    voice = texttospeech.VoiceSelectionParams(
        language_code=request.language_code,
        name=request.voice,
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=resolve_audio_encoding(request.audio_encoding),
        speaking_rate=request.speaking_rate,
        pitch=request.pitch,
    )
    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config,
    )
    return AudioArtifact(
        content=response.audio_content,
        encoding=audio_encoding,
        voice_name=voice_name,
        language_code=language_code,
    )
