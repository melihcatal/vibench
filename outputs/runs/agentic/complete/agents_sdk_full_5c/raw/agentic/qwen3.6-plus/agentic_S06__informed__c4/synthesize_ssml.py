"""
Synthesize SSML with voice and prosody controls using ElevenLabs Text to Speech.

Provider: ElevenLabs Text to Speech
SDK: elevenlabs
Auth: ELEVENLABS_API_KEY
"""

from typing import Optional

from elevenlabs import ElevenLabs

from speech_client import get_elevenlabs_client
from speech_models import SSMLRequest, TTSResponse


def build_ssml(
    text: str,
    voice_style: Optional[str] = None,
    rate: Optional[str] = None,
    pitch: Optional[str] = None,
    volume: Optional[str] = None,
) -> str:
    """Build SSML markup with prosody controls.

    ElevenLabs supports a subset of SSML including break, emphasis, and prosody tags.

    Args:
        text: The base text content.
        voice_style: Optional style tag.
        rate: Speech rate (e.g. 'slow', 'fast', '1.2x').
        pitch: Pitch adjustment (e.g. '+10%', '-2st').
        volume: Volume adjustment (e.g. 'loud', 'soft', '-3dB').

    Returns:
        SSML string ready for synthesis.
    """
    prosody_attrs = []
    if rate:
        prosody_attrs.append(f'rate="{rate}"')
    if pitch:
        prosody_attrs.append(f'pitch="{pitch}"')
    if volume:
        prosody_attrs.append(f'volume="{volume}"')

    inner = text
    if prosody_attrs:
        attrs = " ".join(prosody_attrs)
        inner = f'<prosody {attrs}>{text}</prosody>'

    if voice_style:
        inner = f'<speak><voice name="{voice_style}">{inner}</voice></speak>'
    else:
        inner = f'<speak>{inner}</speak>'

    return inner


def synthesize_ssml(
    ssml_text: str,
    voice_id: Optional[str] = None,
    model_id: Optional[str] = None,
    api_key: Optional[str] = None,
    stability: float = 0.5,
    similarity_boost: float = 0.75,
) -> TTSResponse:
    """Synthesize SSML markup to audio bytes using ElevenLabs.

    Args:
        ssml_text: SSML markup with prosody/voice controls.
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
        text=ssml_text,
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
        character_count=len(ssml_text),
    )


def synthesize_with_prosody(
    text: str,
    voice_id: Optional[str] = None,
    rate: str = "medium",
    pitch: str = "default",
    api_key: Optional[str] = None,
) -> TTSResponse:
    """High-level synthesis with prosody controls.

    Args:
        text: Plain text.
        voice_id: ElevenLabs voice ID.
        rate: Rate control (slow, medium, fast, or multipliers like 1.2x).
        pitch: Pitch control (default, +N%, -Nst, etc.).
        api_key: ElevenLabs API key.

    Returns:
        TTSResponse with synthesized audio.
    """
    ssml = build_ssml(text, rate=rate, pitch=pitch)
    return synthesize_ssml(ssml, voice_id=voice_id, api_key=api_key)
