from __future__ import annotations

from speech_client import build_audio_config, build_synthesis_input, build_voice_params, get_tts_client
from speech_models import SynthesisRequest, SynthesisResult


GOOGLE_TTS_MODEL_FAMILY = "Chirp3-HD"


def synthesize_text(
    text: str,
    language_code: str = "en-US",
    voice_name: str | None = None,
    audio_encoding: str = "MP3",
    speaking_rate: float = 1.0,
    pitch: float = 0.0,
    sample_rate_hertz: int | None = None,
) -> SynthesisResult:
    client = get_tts_client()
    request = SynthesisRequest(
        text=text,
        language_code=language_code,
        voice_name=voice_name,
        audio_encoding=audio_encoding,
        speaking_rate=speaking_rate,
        pitch=pitch,
        sample_rate_hertz=sample_rate_hertz,
    )
    response = client.synthesize_speech(
        input=build_synthesis_input(request),
        voice=build_voice_params(language_code=language_code, voice_name=voice_name),
        audio_config=build_audio_config(
            audio_encoding=audio_encoding,
            speaking_rate=speaking_rate,
            pitch=pitch,
            sample_rate_hertz=sample_rate_hertz,
        ),
    )
    return SynthesisResult(
        audio_bytes=response.audio_content,
        audio_encoding=audio_encoding,
        provider="google-cloud-texttospeech",
        voice_name=voice_name,
        language_code=language_code,
        sample_rate_hertz=sample_rate_hertz,
    )
