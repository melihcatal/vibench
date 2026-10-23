"""Synthesize plain text to an audio byte stream using ElevenLabs Text to Speech."""

from elevenlabs import ElevenLabs

from speech_client import (
    create_elevenlabs_client,
    DEFAULT_MODEL,
    DEFAULT_VOICE_ID,
    DEFAULT_OUTPUT_FORMAT,
)
from speech_models import TTSRequest, TTSResponse


def synthesize_text(
    text: str,
    *,
    voice_id: str = DEFAULT_VOICE_ID,
    model_id: str = DEFAULT_MODEL,
    output_format: str = DEFAULT_OUTPUT_FORMAT,
    stability: float = 0.5,
    similarity_boost: float = 0.75,
    client: ElevenLabs | None = None,
) -> TTSResponse:
    """Synthesize plain text speech using ElevenLabs and return normalized response.

    Uses the ElevenLabs text-to-speech SDK (elevenlabs) to convert
    natural-language text into an audio byte stream.

    Args:
        text: The plain text to synthesize into speech.
        voice_id: ElevenLabs voice identifier (default: Rachel).
        model_id: ElevenLabs model identifier (default: eleven_multilingual_v2).
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
        text=text,
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
        character_count=len(text),
    )
