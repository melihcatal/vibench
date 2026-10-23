from __future__ import annotations

from elevenlabs import VoiceSettings

from speech_client import collect_audio_bytes, get_speech_client, get_speech_config
from speech_models import (
    AudioResult,
    TTSRequest,
    coerce_text,
    normalize_audio_format,
    normalize_locale,
)


def synthesize_text(request: TTSRequest) -> AudioResult:
    config = get_speech_config()
    client = get_speech_client()
    text = coerce_text(request.text)
    locale = normalize_locale(request.locale)
    audio_format = normalize_audio_format(request.audio_format)
    output_format = config.output_format if audio_format == "mp3" else "pcm_44100"
    audio_stream = client.text_to_speech.convert(
        voice_id=request.voice or config.default_voice_id,
        model_id=config.model_id,
        output_format=output_format,
        text=text,
        voice_settings=VoiceSettings(
            stability=0.5,
            similarity_boost=0.75,
            style=max(0.0, min(1.0, abs(request.pitch) / 10.0)),
            use_speaker_boost=True,
            speed=max(0.7, min(1.2, request.speaking_rate)),
        ),
    )
    return AudioResult(
        audio_bytes=collect_audio_bytes(audio_stream),
        audio_format=audio_format,
        voice=request.voice or config.default_voice_id,
        locale=locale,
        metadata={"model_id": config.model_id, "output_format": output_format},
    )
