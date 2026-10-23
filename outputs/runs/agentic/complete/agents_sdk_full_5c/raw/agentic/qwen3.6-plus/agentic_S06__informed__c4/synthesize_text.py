"""
Synthesize plain text to an audio byte stream using ElevenLabs Text to Speech.

Provider: ElevenLabs Text to Speech
SDK: elevenlabs
Auth: ELEVENLABS_API_KEY
"""

from typing import Optional

from elevenlabs import ElevenLabs

from speech_client import get_elevenlabs_client, get_voice_config
from speech_models import TTSRequest, TTSResponse


def synthesize_text(
    text: str,
    voice_id: Optional[str] = None,
    model_id: Optional[str] = None,
    api_key: Optional[str] = None,
    stability: float = 0.5,
    similarity_boost: float = 0.75,
) -> TTSResponse:
    """Synthesize plain text to audio bytes using ElevenLabs.

    Args:
        text: Plain text to synthesize.
        voice_id: ElevenLabs voice ID. Defaults to Rachel (EXAVITQu4vr4xnSDxMaL).
        model_id: ElevenLabs model ID. Defaults to eleven_multilingual_v2.
        api_key: ElevenLabs API key. Falls back to ELEVENLABS_API_KEY env var.
        stability: Voice stability (0.0-1.0).
        similarity_boost: Voice similarity (0.0-1.0).

    Returns:
        TTSResponse with audio bytes and metadata.
    """
    client: ElevenLabs = get_elevenlabs_client(api_key)

    effective_voice = voice_id or "EXAVITQu4vr4xnSDxMaL"
    effective_model = model_id or "eleven_multilingual_v2"

    audio_stream = client.generate(
        text=text,
        voice=effective_voice,
        model=effective_model,
        output_format="mp3_44100_128",
        voice_settings={
            "stability": stability,
            "similarity_boost": similarity_boost,
            "style": 0.0,
            "use_speaker_boost": True,
        },
    )

    audio_bytes = b"".join(chunk for chunk in audio_stream)

    return TTSResponse(
        audio_bytes=audio_bytes,
        content_type="audio/mpeg",
        voice_id=effective_voice,
        model_id=effective_model,
        character_count=len(text),
    )


def synthesize_text_chunked(
    text: str,
    voice_id: Optional[str] = None,
    model_id: Optional[str] = None,
    api_key: Optional[str] = None,
    stability: float = 0.5,
    similarity_boost: float = 0.75,
    chunk_size: int = 4096,
) -> bytes:
    """Synthesize text with streaming/chunked audio output.

    Args:
        text: Plain text to synthesize.
        voice_id: ElevenLabs voice ID.
        model_id: ElevenLabs model ID (e.g. eleven_multilingual_v2).
        api_key: ElevenLabs API key.
        stability: Voice stability.
        similarity_boost: Voice similarity.
        chunk_size: Byte chunk size for streaming.

    Returns:
        Complete audio bytes.
    """
    client: ElevenLabs = get_elevenlabs_client(api_key)

    effective_voice = voice_id or "EXAVITQu4vr4xnSDxMaL"
    effective_model = model_id or "eleven_multilingual_v2"

    audio_stream = client.generate(
        text=text,
        voice=effective_voice,
        model=effective_model,
        output_format="mp3_44100_128",
        stream=True,
        voice_settings={
            "stability": stability,
            "similarity_boost": similarity_boost,
        },
    )

    result = bytearray()
    for chunk in audio_stream:
        result.extend(chunk)
    return bytes(result)
