"""Synthesizes SSML with voice and prosody controls using ElevenLabs TTS API."""

from typing import Optional

from speech_client import (
    configure_speech_settings,
    get_elevenlabs_client,
    resolve_audio_format,
    resolve_model_id,
    resolve_voice_id,
)
from speech_models import SSMLRequest, TTSResponse


def synthesize_ssml(
    ssml: str,
    voice_id: Optional[str] = None,
    model_id: Optional[str] = None,
    output_format: Optional[str] = None,
    stability: Optional[float] = None,
    similarity_boost: Optional[float] = None,
    style: Optional[float] = None,
    use_speaker_boost: Optional[bool] = None,
) -> TTSResponse:
    """Synthesize SSML markup into audio via ElevenLabs.

    The SSML may include <speak>, <voice>, <prosody>, <break/> and other
    ElevenLabs-supported SSML tags to control pitch, rate, volume, and pauses.
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

    request = SSMLRequest(
        ssml=ssml,
        voice_id=resolved_voice,
        model_id=resolved_model,
        output_format=resolved_format,
        settings=settings,
    )

    audio_generator = client.text_to_speech.convert_as_stream(
        voice_id=request.voice_id,
        model_id=request.model_id,
        output_format=request.output_format,
        text=request.ssml,
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
        character_count=len(ssml),
    )


def build_ssml(
    text: str,
    rate: Optional[str] = None,
    pitch: Optional[str] = None,
    volume: Optional[str] = None,
    break_ms: Optional[int] = None,
    emphasis: Optional[str] = None,
) -> str:
    """Build an ElevenLabs-compatible SSML string with optional prosody controls."""
    parts = ['<speak>']

    if break_ms is not None:
        parts.append(f'<break time="{break_ms}ms"/>')

    prosody_attrs = []
    if rate is not None:
        prosody_attrs.append(f'rate="{rate}"')
    if pitch is not None:
        prosody_attrs.append(f'pitch="{pitch}"')
    if volume is not None:
        prosody_attrs.append(f'volume="{volume}"')

    inner_text = _apply_emphasis(text, emphasis)

    if prosody_attrs:
        attrs = " ".join(prosody_attrs)
        parts.append(f'<prosody {attrs}>{inner_text}</prosody>')
    else:
        parts.append(inner_text)

    parts.append('</speak>')
    return "".join(parts)


def _apply_emphasis(text: str, level: Optional[str]) -> str:
    """Wrap text with an emphasis tag if a level is specified."""
    if level and level in ("strong", "moderate", "reduced"):
        return f'<emphasis level="{level}">{text}</emphasis>'
    return text


def synthesize_ssml_from_request(request: SSMLRequest) -> TTSResponse:
    """Synthesize SSML using a pre-built SSMLRequest object via ElevenLabs."""
    return synthesize_ssml(
        ssml=request.ssml,
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
