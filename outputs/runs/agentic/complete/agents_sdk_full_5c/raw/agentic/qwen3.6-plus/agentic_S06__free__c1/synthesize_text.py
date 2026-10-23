"""
synthesize_text.py - Synthesizes plain text to an audio byte stream using ElevenLabs.

Provider: ElevenLabs (https://api.elevenlabs.io)
Model: eleven_multilingual_v2 (default) or eleven_monolingual_v1
SDK: elevenlabs Python package
"""

from typing import Optional

from elevenlabs import generate
from elevenlabs.client import ElevenLabs

from speech_client import get_elevenlabs_client, validate_audio_format, validate_voice_id
from speech_models import TTSRequest, TTSResponse, normalize_speech_text


# Default ElevenLabs model IDs
ELEVEN_MONOLINGUAL_V1 = "eleven_monolingual_v1"
ELEVEN_MULTILINGUAL_V2 = "eleven_multilingual_v2"
ELEVEN_TURBO_V2 = "eleven_turbo_v2"

# Default ElevenLabs voice ID (Rachel)
DEFAULT_VOICE_ID = "21m00Tcm4TlvDq8ikWAM"


def synthesize_text(
    text: str,
    voice_id: str = DEFAULT_VOICE_ID,
    model_id: str = ELEVEN_MULTILINGUAL_V2,
    output_format: str = "mp3_44100_128",
    stability: float = 0.5,
    similarity: float = 0.75,
    style: float = 0.0,
    api_key: Optional[str] = None,
) -> TTSResponse:
    """Synthesize plain text to an audio byte stream using ElevenLabs.

    Args:
        text: Plain text to synthesize.
        voice_id: ElevenLabs voice ID (default: Rachel '21m00Tcm4TlvDq8ikWAM').
        model_id: ElevenLabs model ID (default: 'eleven_multilingual_v2').
        output_format: ElevenLabs audio format (default: 'mp3_44100_128').
        stability: Voice stability (0.0 - 1.0).
        similarity: Voice similarity boost (0.0 - 1.0).
        style: Style exaggeration (0.0 - 1.0).
        api_key: Optional explicit API key override.

    Returns:
        TTSResponse containing audio bytes and synthesis metadata.

    Raises:
        ValueError: If text is empty or parameters are invalid.
        Exception: If ElevenLabs API call fails.
    """
    if not text or not text.strip():
        raise ValueError("Input text cannot be empty.")

    normalized_text = normalize_speech_text(text)
    validate_voice_id(voice_id)
    validate_audio_format(output_format)

    client = get_elevenlabs_client(api_key=api_key)

    audio_bytes = generate(
        text=normalized_text,
        voice=voice_id,
        model=model_id,
        output_format=output_format,
        voice_settings={
            "stability": stability,
            "similarity_boost": similarity,
            "style": style,
            "use_speaker_boost": True,
        },
    )

    if isinstance(audio_bytes, bytes):
        raw_audio = audio_bytes
    else:
        raw_audio = b"".join(audio_bytes) if hasattr(audio_bytes, '__iter__') else bytes(audio_bytes)

    return TTSResponse(
        audio_bytes=raw_audio,
        content_type="audio/mpeg",
        model_id=model_id,
        voice_id=voice_id,
        character_count=len(normalized_text),
    )


def synthesize_text_low_latency(
    text: str,
    voice_id: str = DEFAULT_VOICE_ID,
    api_key: Optional[str] = None,
) -> TTSResponse:
    """Synthesize text using ElevenLabs Turbo model for low latency.

    Uses 'eleven_turbo_v2' model which is optimized for fast streaming.

    Args:
        text: Plain text to synthesize.
        voice_id: ElevenLabs voice ID.
        api_key: Optional explicit API key override.

    Returns:
        TTSResponse with audio bytes.
    """
    return synthesize_text(
        text=text,
        voice_id=voice_id,
        model_id=ELEVEN_TURBO_V2,
        api_key=api_key,
    )


if __name__ == "__main__":
    sample_text = "Hello! This is a test of ElevenLabs text-to-speech synthesis."
    response = synthesize_text(sample_text)
    print(f"Synthesized {response.character_count} characters.")
    print(f"Audio size: {len(response.audio_bytes)} bytes")
    print(f"Model: {response.model_id}")
    print(f"Voice: {response.voice_id}")
