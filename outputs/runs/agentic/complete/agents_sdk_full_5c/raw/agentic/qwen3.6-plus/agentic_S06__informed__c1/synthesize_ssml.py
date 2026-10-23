"""
[SAME-SCENARIO] synthesize_ssml.py
Synthesizes SSML with voice and prosody controls using ElevenLabs TTS API.
ElevenLabs supports SSML via their generate endpoint when the input text
is wrapped in SSML markup.
"""
from typing import Optional, Dict, Any
from elevenlabs import ElevenLabs, Voice, VoiceSettings
from speech_models import SSMLRequest, TTSResponse, AudioFormat
from speech_client import (
    get_elevenlabs_client,
    build_voice_settings,
    resolve_audio_format_key,
    normalize_elevenlabs_response,
    wrap_ssml,
    DEFAULT_ELEVENLABS_MODEL,
    DEFAULT_VOICE,
    DEFAULT_STABILITY,
    DEFAULT_SIMILARITY_BOOST,
)


def synthesize_ssml(
    ssml: str,
    voice_id: Optional[str] = None,
    model_id: str = DEFAULT_ELEVENLABS_MODEL,
    audio_format: AudioFormat = AudioFormat.MP3,
    stability: float = DEFAULT_STABILITY,
    similarity_boost: float = DEFAULT_SIMILARITY_BOOST,
    api_key: Optional[str] = None,
    client: Optional[ElevenLabs] = None,
) -> TTSResponse:
    """
    Synthesize SSML markup to audio using ElevenLabs Text-to-Speech.

    ElevenLabs interprets SSML tags such as <break>, <prosody>, <emphasis>,
    and <say-as> when passed as the input text.

    Args:
        ssml: The SSML markup string (must start with <speak>).
        voice_id: ElevenLabs voice ID.
        model_id: ElevenLabs model ID (e.g., "eleven_multilingual_v2").
        audio_format: Output audio format.
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
        text=ssml,
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


def synthesize_ssml_from_request(
    request: SSMLRequest,
    api_key: Optional[str] = None,
    client: Optional[ElevenLabs] = None,
) -> TTSResponse:
    """Synthesize SSML using a normalized SSMLRequest object."""
    return synthesize_ssml(
        ssml=request.ssml,
        voice_id=request.voice_id,
        model_id=request.model_id,
        audio_format=request.audio_format,
        stability=request.stability,
        similarity_boost=request.similarity_boost,
        api_key=api_key,
        client=client,
    )


def build_ssml_narration(
    text: str,
    voice_name: Optional[str] = None,
    rate: Optional[str] = None,
    pitch: Optional[str] = None,
    volume: Optional[str] = None,
    pause_before: Optional[str] = None,
    pause_after: Optional[str] = None,
) -> str:
    """
    Build an SSML string from plain text with optional prosody and breaks.
    Uses the local wrap_ssml helper and adds <break> tags.
    """
    ssml = wrap_ssml(text, voice_name, rate, pitch, volume)
    parts = []
    if pause_before:
        parts.append(f'<break time="{pause_before}"/>')
    parts.append(ssml.replace("<speak>", "").replace("</speak>", ""))
    if pause_after:
        parts.append(f'<break time="{pause_after}"/>')
    inner = "".join(parts)
    return f"<speak>{inner}</speak>"


if __name__ == "__main__":
    narration_ssml = build_ssml_narration(
        text="Welcome to our presentation.",
        rate="slow",
        pitch="+2st",
        pause_before="500ms",
        pause_after="300ms",
    )
    print(f"Generated SSML: {narration_ssml}")

    result = synthesize_ssml(
        ssml=narration_ssml,
        voice_id="21m00Tcm4TlvDq8ikWAM",
        model_id="eleven_multilingual_v2",
    )
    print(f"Generated {len(result.audio_bytes)} bytes of {result.content_type} audio from SSML.")
