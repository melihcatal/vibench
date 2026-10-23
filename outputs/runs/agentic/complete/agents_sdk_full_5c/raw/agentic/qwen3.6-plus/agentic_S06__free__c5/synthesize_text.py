"""Synthesizes plain text to an audio byte stream using ElevenLabs TTS API."""

from typing import Optional

from speech_client import (
    configure_speech_settings,
    get_elevenlabs_client,
    resolve_audio_format,
    resolve_model_id,
    resolve_voice_id,
)
from speech_models import TTSRequest, TTSResponse


def synthesize_text(
    text: str,
    voice_id: Optional[str] = None,
    model_id: Optional[str] = None,
    output_format: Optional[str] = None,
    stability: Optional[float] = None,
    similarity_boost: Optional[float] = None,
    style: Optional[float] = None,
    use_speaker_boost: Optional[bool] = None,
) -> TTSResponse:
    """Synthesize plain text into an audio byte stream via ElevenLabs.

    Uses the ElevenLabs ElevenLabs class and model "eleven_multilingual_v2"
    to produce spoken audio from the provided text input.
    """
    client = get_elevenlabs_client()

    resolved_voice = resolve_voice_id(voice_id)
    resolved_model = resolve_model_id(model_id)
    resolved_format = resolve_audio_format(output_format)
    settings = configure_speech_settings(
        stability=stability,
        similarity_boost=similarity_boost,
        style=style,
        use_speaker_boost=use_speaker_boost,
    )

    request = TTSRequest(
        text=text,
        voice_id=resolved_voice,
        model_id=resolved_model,
        output_format=resolved_format,
        settings=settings,
    )

    audio_generator = client.text_to_speech.convert(
        voice_id=request.voice_id,
        model_id=request.model_id,
        output_format=request.output_format,
        text=request.text,
        voice_settings=settings if settings else None,
    )

    audio_bytes = b""
    for chunk in audio_generator:
        audio_bytes += chunk

    content_type = _infer_content_type(request.output_format)

    return TTSResponse(
        audio_bytes=audio_bytes,
        content_type=content_type,
        voice_id=request.voice_id,
        model_id=request.model_id,
        character_count=len(text),
    )


def synthesize_text_from_request(request: TTSRequest) -> TTSResponse:
    """Synthesize text using a pre-built TTSRequest object via ElevenLabs."""
    return synthesize_text(
        text=request.text,
        voice_id=request.voice_id,
        model_id=request.model_id,
        output_format=request.output_format,
        **request.settings,
    )


def _infer_content_type(output_format: str) -> str:
    """Map ElevenLabs output format string to an HTTP content-type."""
    if output_format.startswith("mp3"):
        return "audio/mpeg"
    elif output_format.startswith("pcm"):
        return "audio/pcm"
    elif output_format.startswith("ulaw"):
        return "audio/basic"
    return "application/octet-stream"
