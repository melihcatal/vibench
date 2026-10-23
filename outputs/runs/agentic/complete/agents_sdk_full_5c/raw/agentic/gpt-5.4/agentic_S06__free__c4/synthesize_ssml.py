from __future__ import annotations

from google.cloud import texttospeech

from speech_client import get_google_tts_client, resolve_audio_encoding
from speech_models import AudioArtifact, SynthesisRequest


GOOGLE_TTS_PROVIDER = "texttospeech.googleapis.com"


def synthesize_ssml(
    ssml: str,
    language_code: str = "en-US",
    voice_name: str | None = None,
    speaking_rate: float = 1.0,
    pitch: float = 0.0,
    audio_encoding: str = "MP3",
) -> AudioArtifact:
    client = get_google_tts_client()
    request = SynthesisRequest(
        ssml=ssml,
        voice=voice_name,
        language_code=language_code,
        speaking_rate=speaking_rate,
        pitch=pitch,
        audio_encoding=audio_encoding,
    )
    response = client.synthesize_speech(
        input=texttospeech.SynthesisInput(ssml=request.ssml),
        voice=texttospeech.VoiceSelectionParams(
            language_code=request.language_code,
            name=request.voice,
        ),
        audio_config=texttospeech.AudioConfig(
            audio_encoding=resolve_audio_encoding(request.audio_encoding),
            speaking_rate=request.speaking_rate,
            pitch=request.pitch,
        ),
    )
    return AudioArtifact(
        content=response.audio_content,
        encoding=audio_encoding,
        voice_name=voice_name,
        language_code=language_code,
    )
