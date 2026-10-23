from __future__ import annotations

from elevenlabs import VoiceSettings

from speech_client import collect_audio_bytes, get_speech_client, get_speech_config
from speech_models import (
    AudioResult,
    SSMLRequest,
    coerce_text,
    normalize_audio_format,
    normalize_locale,
)


def synthesize_ssml(request: SSMLRequest) -> AudioResult:
    config = get_speech_config()
    client = get_speech_client()
    ssml = coerce_text(request.ssml)
    locale = normalize_locale(request.locale)
    audio_format = normalize_audio_format(request.audio_format)
    output_format = config.output_format if audio_format == "mp3" else "pcm_44100"
    wrapped_text = ssml if "<speak" in ssml else f"<speak>{ssml}</speak>"
    audio_stream = client.text_to_speech.convert(
        voice_id=request.voice or config.default_voice_id,
        model_id="eleven_turbo_v2_5",
        output_format=output_format,
        text=wrapped_text,
        enable_logging=False,
        voice_settings=VoiceSettings(
            stability=0.35,
            similarity_boost=0.8,
            style=0.4,
            use_speaker_boost=True,
            speed=1.0,
        ),
    )
    return AudioResult(
        audio_bytes=collect_audio_bytes(audio_stream),
        audio_format=audio_format,
        voice=request.voice or config.default_voice_id,
        locale=locale,
        metadata={
            "model_id": "eleven_turbo_v2_5",
            "ssml": True,
            "output_format": output_format,
        },
    )
