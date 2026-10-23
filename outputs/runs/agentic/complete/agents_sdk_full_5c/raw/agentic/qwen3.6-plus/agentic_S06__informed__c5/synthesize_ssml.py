"""Synthesize SSML with voice and prosody controls using ElevenLabs Text to Speech."""

from elevenlabs import ElevenLabs

from speech_client import (
    create_elevenlabs_client,
    DEFAULT_MODEL,
    DEFAULT_VOICE_ID,
    DEFAULT_OUTPUT_FORMAT,
)
from speech_models import TTSRequest, TTSResponse


def build_ssml_text(
    text: str,
    voice_name: str = "Rachel",
    pitch: str = "default",
    rate: str = "medium",
    volume: str = "default",
) -> str:
    """Build an SSML-wrapped text string for ElevenLabs synthesis.

    Wraps the input text in SSML with prosody controls for pitch, rate,
    and volume. ElevenLabs' model supports SSML-like break and emphasis tags
    which this helper formats.

    Args:
        text: The plain text content to wrap.
        voice_name: Reference voice label for SSML context.
        pitch: Pitch adjustment (default, x-low, low, medium, high, x-high).
        rate: Speaking rate (default, x-slow, slow, medium, fast, x-fast).
        volume: Volume level (default, silent, x-soft, soft, medium, loud, x-loud).

    Returns:
        A formatted SSML string.
    """
    ssml_parts = []
    ssml_parts.append('<speak>')
    ssml_parts.append(
        f'<prosody pitch="{pitch}" rate="{rate}" volume="{volume}">'
    )
    ssml_parts.append(text)
    ssml_parts.append('</prosody>')
    ssml_parts.append('</speak>')
    return "\n".join(ssml_parts)


def synthesize_ssml(
    ssml_text: str,
    *,
    voice_id: str = DEFAULT_VOICE_ID,
    model_id: str = DEFAULT_MODEL,
    output_format: str = DEFAULT_OUTPUT_FORMAT,
    stability: float = 0.5,
    similarity_boost: float = 0.75,
    client: ElevenLabs | None = None,
) -> TTSResponse:
    """Synthesize SSML-marked text into speech audio using ElevenLabs.

    Uses the ElevenLabs TTS SDK (elevenlabs) to convert SSML-formatted text
    with prosody and voice controls into an audio byte stream.

    Args:
        ssml_text: SSML-formatted text including prosody tags.
        voice_id: ElevenLabs voice identifier (default: Rachel).
        model_id: ElevenLabs model (default: eleven_multilingual_v2).
        output_format: Audio output format string.
        stability: Voice stability factor (0.0–1.0).
        similarity_boost: Voice similarity boost factor (0.0–1.0).
        client: Optional pre-configured ElevenLabs client instance.

    Returns:
        TTSResponse containing the synthesized audio bytes and metadata.
    """
    if client is None:
        client = create_elevenlabs_client()

    request = TTSRequest(
        text=ssml_text,
        model_id=model_id,
        voice_id=voice_id,
        output_format=output_format,
        stability=stability,
        similarity_boost=similarity_boost,
    )

    audio_stream = client.text_to_speech.convert(
        voice_id=voice_id,
        model_id=model_id,
        output_format=output_format,
        text=request.text,
        voice_settings={
            "stability": request.stability,
            "similarity_boost": request.similarity_boost,
        },
    )

    audio_bytes = b"".join(chunk for chunk in audio_stream)

    return TTSResponse(
        audio_bytes=audio_bytes,
        content_type="audio/mpeg",
        model_id=model_id,
        voice_id=voice_id,
        character_count=len(ssml_text),
    )
