"""
[SAME-SCENARIO] synthesize_text.py
Synthesizes plain text to an audio byte stream using ElevenLabs TTS API.
"""
from typing import Optional, Dict, Any
from elevenlabs import ElevenLabs, VoiceSettings
from speech_models import TTSRequest, TTSResponse, AudioFormat
from speech_client import (
    get_elevenlabs_client,
    build_voice_settings,
    resolve_audio_format_key,
    normalize_elevenlabs_response,
    DEFAULT_ELEVENLABS_MODEL,
    DEFAULT_VOICE,
    DEFAULT_STABILITY,
    DEFAULT_SIMILARITY_BOOST,
)


def synthesize_text(
    text: str,
    voice_id: Optional[str] = None,
    model_id: str = DEFAULT_ELEVENLABS_MODEL,
    audio_format: AudioFormat = AudioFormat.MP3,
    speed: float = 1.0,
    pitch: float = 0.0,
    stability: float = DEFAULT_STABILITY,
    similarity_boost: float = DEFAULT_SIMILARITY_BOOST,
    api_key: Optional[str] = None,
    client: Optional[ElevenLabs] = None,
) -> TTSResponse:
    """
    Synthesize plain text to audio using ElevenLabs Text-to-Speech.

    Args:
        text: The plain text to synthesize.
        voice_id: ElevenLabs voice ID (e.g., "21m00Tcm4TlvDq8ikWAM" for Rachel).
        model_id: ElevenLabs model ID (e.g., "eleven_multilingual_v2", "eleven_turbo_v2_5").
        audio_format: Output audio format.
        speed: Speech speed multiplier (not directly supported; stored in metadata).
        pitch: Speech pitch shift (not directly supported; stored in metadata).
        stability: Voice stability (0.0 to 1.0).
        similarity_boost: Voice similarity boost (0.0 to 1.0).
        api_key: Optional ElevenLabs API key.
        client: Optional pre-built ElevenLabs client.

    Returns:
        TTSResponse with audio bytes and metadata.
    """
    if client is None:
        client = get_elevenlabs_client(api_key)

    target_voice = voice_id or DEFAULT_VOICE
    voice_settings = build_voice_settings(stability, similarity_boost)
    output_format = resolve_audio_format_key(audio_format)

    audio_chunks = client.generate(
        text=text,
        voice=Voice(
            voice_id=target_voice,
            settings=voice_settings,
        ),
        model=model_id,
        output_format=output_format,
    )

    audio_bytes = b"".join(chunk for chunk in audio_chunks)

    return normalize_elevenlabs_response(
        audio_bytes=audio_bytes,
        voice_id=target_voice,
        model_id=model_id,
        audio_format=audio_format,
    )


def synthesize_from_request(
    request: TTSRequest,
    api_key: Optional[str] = None,
    client: Optional[ElevenLabs] = None,
) -> TTSResponse:
    """Synthesize text using a normalized TTSRequest object."""
    return synthesize_text(
        text=request.text,
        voice_id=request.voice_id,
        model_id=request.model_id,
        audio_format=request.audio_format,
        speed=request.speed,
        pitch=request.pitch,
        stability=request.stability,
        similarity_boost=request.similarity_boost,
        api_key=api_key,
        client=client,
    )


if __name__ == "__main__":
    result = synthesize_text(
        text="Hello, this is a test of ElevenLabs text-to-speech synthesis.",
        voice_id="21m00Tcm4TlvDq8ikWAM",
        model_id="eleven_multilingual_v2",
    )
    print(f"Generated {len(result.audio_bytes)} bytes of {result.content_type} audio.")
